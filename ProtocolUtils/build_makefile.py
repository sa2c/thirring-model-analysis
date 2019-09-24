#!/usr/bin/env python3

import re
from os import path
from sys import exit,argv,stdout, stderr

# LISTING EXECUTABLES

exeExts = ['.sh', '.py', ]

# LOOKING FOR LOGFILES

logExt = '.log'

setExts = ['.set', '.conf' ] 

# location of the log command
logcommand = '../ProtocolUtils/log'

# lib location
lib_load_command = '. ../Scripts/lib.sh'

# MAKE TARGETS: a dictionary
# key: name of the output file
# value: input files, and the command line 


oldMakeTargets = dict()
oldGroupMakeNodes = []

makeTargets = dict()    # [output ] =          inputs, command
groupMakeNodes = dict() # [logfile] = outputs, inputs, command

bePedantic = False

if '--pedantic' in argv:
    bePedantic = True
    argv.remove( '--pedantic')

grouping = True

def scanLogFile(logFile):
    print("scanning "+logFile)
    inputs = []
    outputs = []
    f = open(logFile,'r')
    basedir = path.dirname(logFile)
    if path.basename(basedir) == 'logs': 
        # then we have read the logfile from a comprehensive 'logs' directory
        basedir = path.dirname(basedir)
    if basedir == '':
        basedir = '.'
    lines = f.readlines()
    print("COMMAND: " + lines[0][:-1])
    for line in lines:
        if len(line.split()) > 0:
            if line.split()[0] in ['Reading', 'reading', 'Lettura', 'lettura'] :
                search_for_shell_command = re.search(
                        '(\$\()\s*(shell)\s+(find)\s+(.*)(\))',line )
                if search_for_shell_command is not None:
                    groups = search_for_shell_command.groups()
                    assert len(groups) == 5
                    #NOTE:Make is complicated with spaces. 
                    #    'shell' must follow '(' without space(s) in between.
                    thingToAppend = (groups[0]+ #'(' 
                            groups[1]+' '       #'shell '
                            +groups[2]+' '      #'find '   
                            +groups[3]+groups[4]#<arguments to find>)
                            )
                else:
                    thingToAppend = basedir+'/'+line.split()[-1]
                if thingToAppend in inputs:
                    print("'{}' is already in inputs.".format(thingToAppend))
                else:
                    inputs.append(thingToAppend)
            if line.split()[0] in ['Writing', 'writing', 'Scrittura', 'scrittura'] :
                thingToAppend = basedir+'/'+line.split()[-1]
                if thingToAppend in outputs:
                    print("'{}' is already in outputs.".format(thingToAppend))
                else:
                    outputs.append(thingToAppend)
            
    command =  '&&'.join([
        lib_load_command,
        ' '.join(['cd', basedir]),
        ' '.join([logcommand,lines[0]])
        ])


    if len(outputs) == 0:
        print("ERROR in logfile {}, no output file(s) found!".format(logFile))
    else:
        if bePedantic:
            inputs.append(basedir+'/'+lines[0].split()[0])
        groupMakeNodes[logFile] = set(outputs), set(inputs), command
    
        for output in outputs: 
            if output in makeTargets:
                print("ERROR: either there are two ways to produce the same file, or something strange happened!\n")
                print("Same file: {}\n".format(output))
                exit(1)
    
            makeTargets[output] = set(inputs) , command



def compileMakeFile(filename):
    makefile = open(filename,'w')

    def write_long_line(things):
        lineLength = 0
        for thing in things:
            if lineLength+len(thing) > 90:
                makefile.write('\\\n')
                lineLength = 0
            makefile.write(' '+thing)
            lineLength +=len(thing)

    makefile.write('SHELL = bash\n\n')
    makefile.write('all: ')
    keys = list(makeTargets.keys())
    keys.sort()

    write_long_line(keys)

    makefile.write('\n\n')

    if grouping:
        keys = list(groupMakeNodes.keys())
        keys.sort()
        for key in keys:
            outputFiles = list(groupMakeNodes[key][0])
            outputFiles.sort()
            write_long_line(outputFiles)
            makefile.write(' : ')

            inputFiles = list(groupMakeNodes[key][1])
            inputFiles.sort()
            write_long_line(inputFiles)
            makefile.write('\n\t'+groupMakeNodes[key][2]+'\n')

    else:
        keys = list(makeTargets.keys())
        keys.sort()
        for key in keys:
            makefile.write(key+' : ')
            for inputfile in makeTargets[key][0]:
                makefile.write(inputfile+' ')
            makefile.write('\n\t'+makeTargets[key][1]+'\n')



def scanExistingMakefile(fileName):
    f = open(fileName)
    text = f.read()
    newText = text.replace('\\\n','').replace('SHELL = bash\n\n','')
    while '\n\n\n' in newText:
        newText = newText.replace('\n\n\n','\n\n')
    groups = newText.split('\n\n');
    
    while '' in groups:
        groups.remove('')

    def split_inputs(input_string):
        shell_commands = re.findall('\$\(shell[^(]*\)', input_string)

        for shell_command in shell_commands:
            input_string = input_string.replace(shell_command,'')

        return input_string.split() + shell_commands

    for group in groups[1:]: # removing 'all' target, which is the first 
        try : 
            outputsAndInputs, command = group.split('\n')
        except ValueError as e:
            print("An Error occurred.")
            print(e);
            print(group)
            raise e;
        command = command[1:]+'\n'
        try:
            outputs, inputs = outputsAndInputs.split(" : ") 
        except Exception as e:
            print("ERROR")
            print(outputsAndInputs)
            raise e
        outputs = [s for s in outputs.split(' ') if s not in ['',' '] ]
        inputs = split_inputs(inputs)
        if inputs[-1] == '':
            inputs = inputs[:-1]

        oldGroupMakeNodes.append((set(outputs),set(inputs),command))

        for output in outputs: 
            if output in oldMakeTargets:
                print("ERROR: either there are two ways to produce the same file, or something strange happened!\n")
                print("Same file: {}\n".format(output))
                exit(1)
    
            oldMakeTargets[output] = set(inputs) , command
    print("Old Make Targets: {}".format(len(oldMakeTargets)))
    
    #end for groups

def addOldTargetsToNew():

    commandToGroup = dict()

    for logFile in groupMakeNodes: # creating reverse dictionary
        outputs,inputs, command = groupMakeNodes[logFile]
        commandToGroup[command] = logFile
        
    newOldGroupIndex = 0 # new groups coming from old makefile but not visible in logs
    for oldGroupMakeNode in oldGroupMakeNodes:
        oldOutputs,oldInputs,oldCommand = oldGroupMakeNode
        
        
        nonVoidIntersectionCount = 0
        for logFile in groupMakeNodes:
            outputs,inputs,command = groupMakeNodes[logFile]
            if len(outputs & oldOutputs) != 0:
                if command == oldCommand and nonVoidIntersectionCount == 0:
                    inputs.update(oldInputs)
                    outputs.update(oldOutputs)
                    nonVoidIntersectionCount =  1
                elif command != oldCommand:
                    print("Error: new logfile {} is not compatible with old makefile."\
                            .format(commandToGroup[command]))
                    print("Commands not compatible:")
                    print("old: {}".format(oldCommand))
                    print(len(oldCommand))
                    print("new: {}".format(command))
                    print(len(command))
                    exit(1)
                elif nonVoidIntersectionCount != 0 :
                    print("Error: group in old makefile intersects more than one new group.")                 
                    print("old command: {}".format(oldCommand))
                    print("new command: {}".format(command))
                    exit(1)
        #end for 
        if nonVoidIntersectionCount == 0 :
            newOldGroupIndex += 1
            groupMakeNodes[str(newOldGroupIndex)] = oldOutputs,oldInputs,oldCommand

    # now all groups are updated
    makeTargets.clear()
    for key in groupMakeNodes:
        outputs,inputs,command = groupMakeNodes[key]
        for output in outputs:
            makeTargets[output] = set(inputs),command
    print("New makeTargets len() {}".format(len(makeTargets)))
        





if __name__ == '__main__':


    makefileName = 'makefile'
    if not '.log' in argv[1]:
        makefileName = argv[1]
        argv.remove(argv[1])

    for filename in argv[1:]:
        scanLogFile(filename)
    print("Number of makeTargets found in log files: {}".format(len(makeTargets)))

    makeTargetFromLogSet = set(makeTargets.keys())
   
    doNothing = False

    if path.exists(makefileName):
        ans = ''
        possibleAnswers = [ 'yes','no','update','1','2','3' ]
        while ans not in possibleAnswers:
            print("Overwrite makefile? Possible choices:")
            print("1. 'yes' 2. 'no' 3. 'update' ( but check before)")
            print("Notice that you can select another name for the makefile.")
            print("The first argument not ending in '.log' will be taken as the name of ")
            print("the new makefile. Type 'update' or '3' for more info.")
            ans = input().lower()
            if ans not in possibleAnswers:
                print("Please type one of the possible answers:")
                for answ in possibleAnswers:
                    stdout.write(answ)
                stdout.write("\n")

        if ans in ('no','2'):
            print("Stop!")
            exit(0)
        if ans in ('update','3'):
            scanExistingMakefile(makefileName)
            oldMakeTargetSet = set(oldMakeTargets.keys())
            onlyInOldMakeTargetSet = oldMakeTargetSet - makeTargetFromLogSet
            onlyInMakeTargetFromLogSet = makeTargetFromLogSet - oldMakeTargetSet
            interSection = makeTargetFromLogSet & oldMakeTargetSet
            print("No of targets only in old makefile: {}"\
                    .format(len(onlyInOldMakeTargetSet)))
            print("No of targets only logFiles read: {}"\
                    .format(len(onlyInMakeTargetFromLogSet)))
            print("No of targets in intersection: {}"\
                    .format(len(interSection)))
            addOldTargetsToNew()

            loop = True
            while loop:
                print("Now you can:")
                print("1. Go on and write the updated makefile")
                print("2. Print a list of files with infos: ")
                print(" a.the list of the old make targets 'OLD' ")
                print(" b.the list of the make targets found in logfiles 'LOG'")
                print(" c.the intersection 'OLD&LOG'")
                print(" d.'OLD-LOG' ")
                print(" f.'LOG-OLD' ")
                print("3. Exit")
                ans = ''
                thingsToPrint = [ oldMakeTargetSet, makeTargetFromLogSet, interSection, onlyInOldMakeTargetSet, onlyInMakeTargetFromLogSet]
                defFileNames = [ 'allOld.txt', 'allFromLogs.txt', 'intersection.txt',\
                        'onlyOld.txt', 'onlyFromLogs.txt']
                while ans not in [str(e) for e in range(1,4)]:
                    stdout.write("Choose 1-3:")
                    ans = input().lower()
                    if ans == '1' :
                        loop = False
                    elif ans == '2':
                        stdout.write("Ok, filename prefix: ")
                        fileNamePrefix = input()
                        for fileName, thingToPrint in zip(defFileNames, thingsToPrint):
                            fileName = fileNamePrefix + fileName
                            print("Writing {}".format(fileName))
                            with open(fileName,'w') as f:
                                for t in thingToPrint:
                                    f.write(str(t) + '\n')
                    elif ans == '3':
                        loop = False
                        print("Ok, exiting!")
                        doNothing = True
                        


    if not doNothing :
        compileMakeFile(makefileName)


