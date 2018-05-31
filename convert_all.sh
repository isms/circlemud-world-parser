#!/bin/sh
for type in "mob" "obj" "shp" "wld" "zon"; do
    # make the empty folder
    mkdir -p _output/$type

    # get the filenames for each file type
    input_dir=$1
    files=$( find $input_dir -name "*.$type" )

    # convert the files
    for file in $files; do
        number=$( echo $file | cut -d "/" -f 3 | cut -d "." -f 1 )
        output="_output/$type/$number.json"
        echo parsing $file to $output
        python src/parse.py --dest $output $file
    done
done
