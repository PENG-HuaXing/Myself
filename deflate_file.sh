listdir
file_num=$[ $(ll | wc -l)-1 ]
zip_file(){
	echo ""$(echo "$1" | sed 's/$/&.zip/')"-->"$1"-->$(date)" >>  deflate_log.txt
	zip -r "$(echo "$1" | sed 's/$/&.zip/')" "$1" | tee -a deflate_log.txt
}
rar_file(){                                                                                                                                                                                  
         echo ""$(echo "$1" | sed 's/$/&.rar/')"-->"$1"-->$(date)" >>  deflate_log.txt                                                                                                         
	 rar a -r "$(echo "$1" | sed 's/$/&.rar/')" "$1" | tee -a deflate_log.txt  
}     
for ((i=0;i<$file_num;i++))
{
	if [ -d "${file_name_list[$i]}" ] && [ "${file_name_list[$i]}" != "原始文件" ]
	then
		echo "这是一个文件夹,进行压缩操作"
		zip_file "${file_name_list[$i]}"
	fi
}
mkdir "中间文件"
for ((i=0;i<$file_num;i++))
{
	if [ "${file_name_list[$i]}" != "原始文件" ] && [ "${file_name_list[$i]}" != "deflate_file.sh" ] && [ "${file_name_list[$i]}" != "extract_zip_rar.sh" ]
	then
		mv "${file_name_list[$i]}" "中间文件"
	fi
}


