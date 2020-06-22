#!/bin/bash
listdir
file_num=$[ $(ll | wc -l)-1 ]
for ((i=0;i<${file_num};i++))
{
	
	if [ -n "$(echo "${file_name_list[$i]}" | egrep "zip$")" ]
	then

		echo -e "正在检测文件 ${file_name_list[$i]} 的完整性......" | tee -a log.txt
		zip -T "${file_name_list[$i]}" | tee -a log.txt
		echo "" | tee -a log.txt

	elif [ -n "$(echo "${file_name_list[$i]}" | egrep "rar$")" ]
	then
		echo -e "正在检测文件 ${file_name_list[$i]} 的完整性......" | tee -a log.txt 
		rar t "${file_name_list[$i]}" | tee -a log.txt  
		echo "" | tee -a log.txt	
	fi

}
