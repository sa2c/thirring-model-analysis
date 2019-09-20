



cycle(){
  DIRROOT=$1
  shift
  FUN=$1
  shift
  for Ls in 32 40 48
  do
    for beta in $(LANG=en_us seq 0.30 0.02 0.60)
    do
      for m in $(LANG=en_us seq 0.01 0.01 0.05)
      do
        DIRBASENAME=Ls$Ls.beta$beta.m$m
        ../ProtocolUtils/log $FUN $DIRROOT/$DIRBASENAME $@
      done
    done
  done
}



stitch_together(){
  DIR=$1
  OUTPUT_DIR=$2
  TAG=$3

  mkdir -p $OUTPUT_DIR

  for file in fort.11 fort.200
  do 
    TOTAL_FILE=$OUTPUT_DIR/$file.total.$TAG
    echo Writing $TOTAL_FILE
    TOTAL_FILE_CSV=$OUTPUT_DIR/$file.total.$TAG.csv
    echo Writing $TOTAL_FILE_CSV
    if [ "$file" == fort.11 ]
    then 
      HEADERCSV="Timestamp,isweep,gaction,paction"
    elif [ "$file" == fort.200 ]
    then
      HEADERCSV="Timestamp,psibarpsi,susclsing"
    fi
    if [ -f "$TOTAL_FILE" ]
    then
      rm $TOTAL_FILE 
    fi
    touch $TOTAL_FILE 
    echo $HEADERCSV > $TOTAL_FILE_CSV
    echo 'Reading $(shell find '$DIR' -name '"'"'fort.*'"'"')'
    for dir in $(ls -d $DIR/save*/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] | sort -n)
    do
      PREFIX=$(basename $dir)
      awk '{print '$PREFIX',$0}' $dir/$file >> $TOTAL_FILE
      awk '{OFS=",";printf("%s%s",'$PREFIX',OFS);for(i=1;i<=NF;i++)printf("%s%s",$i,i==NF?"\n":OFS)}' $dir/$file >> $TOTAL_FILE_CSV

    done
  done
}


stitch_together_output_dir(){
  DIR=$1
  DIRBASENAME=$(basename $DIR)

  if [[ $DIR == *"thirring_runs"* ]]
  then
    DIR_STEM=all_dirs
  elif [[ $DIR == *'16'* ]] 
  then
    DIR_STEM=all_dirs16
  else 
    exit 
  fi
  echo ../Analysis/$DIR_STEM/$DIRBASENAME
}

stitch_together_wrapper(){
  DIR=$1
  TAG=$2
  if [ -d "$DIR" ] 
  then
     OUTPUT_DIR=$(stitch_together_output_dir $DIR)
     stitch_together $DIR $OUTPUT_DIR $TAG
  fi
}


stitch_together_all(){

  cycle ../Data/thirring_runs1/all_dirs stitch_together_wrapper 1 
  cycle ../Data/thirring_runs2/all_dirs stitch_together_wrapper 2

}

stitch_together_16(){

  cycle ../Data/16/all_dirs stitch_together_wrapper 1 

}


export -f cycle stitch_together stitch_together_wrapper stitch_together_16
