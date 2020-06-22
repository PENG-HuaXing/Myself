#!/bin/bash
listdir
file_num=$[ $(ll | wc -l)-1 ]
for ((i=0;i<${file_num};i++))
{
	
	if [ -n "$(echo "${file_name_list[$i]}" | egrep "zip$")" ]
	then
		if [ -n "$(unzip -l "${file_name_list[$i]}" | grep "/")" ]
		then
			echo "${file_name_list[$i]}"
			echo "该文件可以直接解压"
			echo "${file_name_list[$i]} --> $(date)" >> log.txt
			unzip "${file_name_list[$i]}" | tee -a log.txt
		else
			
			echo "${file_name_list[$i]}"
			echo "该文件buneng可以直接解压!!!!!!!!!!!!!!"
			dirname=$(echo "${file_name_list[$i]}" | sed 's/.zip//g')
			mkdir "$dirname"
			echo "${file_name_list[$i]} --> $(date)" >> log.txt

			unzip "${file_name_list[$i]}" -d "$dirname" | tee -a log.txt
		fi
	elif [ -n "$(echo "${file_name_list[$i]}" | egrep "rar$")" ]
	then
		if [ -n "$(rar l "${file_name_list[$i]}" | grep "/")" ]
		then
			
			echo "${file_name_list[$i]}"
			echo "该文件可以直接解压"
			echo "${file_name_list[$i]} --> $(date)" >> log.txt
			rar x  "${file_name_list[$i]}" | tee -a log.txt
		else
			
			echo "${file_name_list[$i]}"
			echo "该文件buneng直接解压!!!!!!!!!!!!!!!"
			dirname=$(echo "${file_name_list[$i]}" | sed 's/.rar//g')
			mkdir "$dirname"
			echo "${file_name_list[$i]} --> $(date)" >> log.txt

			rar x  "${file_name_list[$i]}"  "$dirname" | tee -a log.txt
		fi
	else
		echo "${file_name_list[$i]}" 
		echo "这个不是可解压文件"
	fi
}
mkdir "原始文件"
for ((i=0;i<${file_num};i++)) 
{
	mv "${file_name_list[$i]}" 原始文件
}
mv 原始文件/extract_zip_rar.sh .
mv 原始文件/deflate_file.sh .
