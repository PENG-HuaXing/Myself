#!/bin/bash

file_name="$1"
statecode=1
if [ -f "$file_name" ]
then
    echo "这是个文件"
    while [ $statecode -eq 1 ]
    do
        info=(`ls -l | grep "$file_name"`)
        begin_size=${info[4]}
        sleep 5
        info=(`ls -l | grep "$file_name"`)
        end_size=${info[4]}
        speed=`echo "scale=3;(${end_size}-${begin_size})/5/1024" | bc`
        #speed=`echo "scale=3;(${end_size}-${begin_size})/5/1024/1024" | bc`
        echo "$speed KB/s"
    done
fi

if [ -d "$file_name" ]
then
    echo "这是个文件夹"
    while [ $statecode -eq 1 ]
    do
        info=(`du -s "$file_name"`)
        begin_size=${info[0]}
        sleep 5
        info=(`du -s "$file_name"`)
        end_size=${info[0]}
        speed=`echo "scale=3;(${end_size}-${begin_size})/5" | bc` 
        #speed=`echo "scale=3;(${end_size}-${begin_size})/5/1024" | bc`
        echo "$speed KB/s"
    done
fi
