#!/bin/bash

check_file_columns(){
    file_to_check=$1
    no_of_cols=$2

    if [ $(awk '{print NF}' $file_to_check | sort -u | wc -l ) -ne 1 ]
    then
        echo "$(date) - Issue with number of fields! - $file_to_check" | tee -a errors.txt
        exit 1
    fi
    if [ $(awk '{print NF}' $file_to_check | sort -u | head -n 1 ) -ne "$no_of_cols" ]
    then
        echo "$(date) - Wrong number of columns! - $file_to_check" | tee -a errors.txt
        exit 2
    fi
}

export -f check_file_columns
