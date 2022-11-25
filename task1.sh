#!/usr/bin/env bash

# get list of all files
# -depth: recursively through the tree
# -type f: list files only (dirs excluded)
list_of_target_files=`find "$1" -depth -type f`


for path in $list_of_target_files
do
    # get a name of a file
    filename=`basename "${path}"`

    # check whether our file contains any capital letters
    if [[ "$filename" =~ [A-Z] ]]

    # if so - go into
    then
        # separate a name of a directory to avoid 'tr' renaming
        dirname=`dirname "${path}"`

        # get a name of a file and translate any capital letters to lower case
        filename=`basename "${path}" | tr '[A-Z]' '[a-z]'`

        # concatenate non-changed dirname with changed filename
        dest=$dirname"/"$filename

        # move from old path to a new lowercase-name file
        was_renamed="$(tput setaf 1)${path} $(tput setaf 4)was renamed to$(tput setaf 2) ${dest}"
        mv $path $dest && echo $was_renamed
    fi
done


# quick test it
#mkdir tesT tesT/QwEr tesT/just_fine
#touch ./tesT/asdfasdJFJASUHJF.dasEE ./tesT/tesT.txTT ./tesT/QwEr/tesTR.T ./tesT/QwEr/test_normal.txt ./tesT/just_fine/shouldnt_be_appeared.txt
