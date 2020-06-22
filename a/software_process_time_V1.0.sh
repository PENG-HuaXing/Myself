#!/bin/bash
timestart="$(date)"
sign=1
softwarename=hadd
while [ $sign -eq 1 ]
do 
	if [ -n "$(top -b -n 1 | grep ${softwarename})" ]	
	then
		sleep 5
	else
		break
	fi
done
timeend="$(date)"

echo -e "软件:${softwarename}\n开始于:${timestart}\n结束于:${timeend}" > timerecorde.txt
mplayer '/mnt/CloudMusic/詩音 - you -ありがとう-.mp3'	
