#!/bin/bash
#how to use
#(1)cmd <passwd> <rar or 7z filename>
#(2)cmd <rar or 7z filename>
#this bash script can change rar or 7z file to zip
#to avoid remove original file by mastake, original file and zip file will all exit when change has done

echo "Helo"
if [ $# -eq 2 ] && [ -n "$(echo "$2" | grep 'rar$')" ]
then
	filename=$(echo "$2" | sed 's/.rar//')
	mkdir "$filename"
	rar x -p"$1" $2 ./"$filename"
	cd "$filename"
	zip -r "$filename".zip ./*
	mv ../"$2" .
fi
echo "one"

if [ $# -eq 2 ] && [ -n "$(echo "$2" | grep '7z$')" ]
then
        filename=$(echo "$2" | sed 's/.7z//')
        mkdir "$filename"
        7z x -p"$1" $2 -o./"$filename"
	cd "$filename"
        zip -r "$filename".zip ./*
        mv ../"$2" .
fi
echo "two"
	
if [ $# -eq 1 ] && [ -n "$(echo "$1" | grep 'rar$')" ]
then    
	echo $1
        filename=$(echo "$1" | sed 's/.rar//')
        mkdir "$filename"
        rar x  "$1" ./"$filename"
	cd "$filename"
        zip -r "$filename".zip ./*
	mv "$filename".zip ..
        trash ../"$1"
	cd ..
	trash "$filename"
fi

echo "three"

if [ $# -eq 1 ] && [ -n "$(echo "$1" | grep '7z$')" ]
then
        filename=$(echo "$1" | sed 's/.7z//')
        mkdir "$filename"
        7z x  "$1" -o./"$filename"
        cd "$filename"
        zip -r "$filename".zip ./*
	mv "$filename".zip ..
        trash ../"$1"
	cd ..
	trash "$filename"

fi
echo "four"


