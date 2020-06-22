#!/bin/bash
timestart="$(date)"
sign=1
softwarename=tpt
while [ $sign -eq 1 ]
do 
	software_status=(`top -b -n 1 | grep "$softwarename"`)
	if [ `echo "${software_status[8]}>100" | bc` -eq 1 ]	
	then
		sleep 5
	else
		break
	fi
done
timeend="$(date)"

echo -e "软件:${softwarename}\n开始于:${timestart}\n结束于:${timeend}" > timerecorde.txt
mplayer '/mnt/CloudMusic/詩音 - you -ありがとう-.mp3'
	
