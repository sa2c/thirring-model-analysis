#!/bin/bash

LsBetaMregex='Ls([0-9]+)\.beta([01]\.[0-9]+)\.m(0\.[0-9]+)'

# for use in analysis file splitter
LsBetaM_from_dirLsBetaM(){

    singleLsBetaM_from_dirLsBetaM(){
          dirLsBetaM=$1
          read Ls beta m <<<$(echo $dirLsBetaM | sed -r 's|.*'$LsBetaMregex'.*|\1 \2 \3|')
          Ls=$(echo $Ls | awk '{printf("%d\n",$1)}')
          beta=$(echo $beta | awk '{printf("%f\n",$1)}')
          m=$(echo $m | awk '{printf("%f\n",$1)}')
          echo $Ls $beta $m
      }
 
   if [ $# -eq 1 ]
   then 
       singledirLsBetaM=$1
       singleLsBetaM_from_dirLsBetaM $singledirLsBetaM
   else
       while read singledirLsBetaM
       do 
          singleLsBetaM_from_dirLsBetaM $singledirLsBetaM
       done
   fi

}


dirLsBetaM_from_LsBetaM(){
    Ls=$1
    beta=$2
    m=$3
    echo Ls$Ls.beta$beta.m$m

}

select_lines_matching_LsBetaM(){
    # grep-like behaviour
    LsBetaM=$1
    filename=$2
    read Ls beta m <<< $(LsBetaM_from_dirLsBetaM $LsBetaM)


    tmp_filename=/tmp/$(date +"%s")_select_lines_matching_LsBetaM

    grep -E "$LsBetaMregex" $filename > $tmp_filename.lines
    sed -r 's|.*'$LsBetaMregex'.*|\1 \2 \3|' $tmp_filename.lines > $tmp_filename.values

    paste $tmp_filename.values $tmp_filename.lines > $tmp_filename.all

    awk '($1=='$Ls' && $2=='$beta' && $3=='$m'){for(i = 4; i <= NF; i++) printf("%s\t", $i) ; printf("\n");}' $tmp_filename.all > $tmp_filename.result

    totlines=$(cat $tmp_filename.result | wc -l)

    if [ $totlines -eq 0 ] 
    then
        exit 1
    fi
    cat $tmp_filename.result

    #rm $tmp_filename.{lines,values,all,result}

}

export -f select_lines_matching_LsBetaM LsBetaM_from_dirLsBetaM
