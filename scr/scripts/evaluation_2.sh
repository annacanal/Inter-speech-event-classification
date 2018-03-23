#!/bin/bash


red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`


if [ $# -ne 1 ] 
   then echo "${red}Enter the path of the file with the predictions${reset}"
   		read path_prediction 
else
    path_prediction=$1 
    echo ${path_prediction};
fi


cat ${path_prediction} | cut -d ',' -f2,3,4,5 > file.txt

cat file.txt | sed s/','/'\ '/g > file2.txt

cat file2.txt > file3.txt

predi=`echo ${path_prediction} | cut -d '/' -f7,8`
output_file="C-E_evaluation_data_structure_geco_unsup_${predi}_b0-3_c4.csv"

echo "pause,file,convo,speaker,pause_onset,pause_offset,Z_click,Auto_click,Z_breath,Auto_breath" > ${output_file}



temp_start=0
zero=0

sum_bre=0
sum_clicks=0

prev_click=false
prev_bre=false

sum_0=0
sum_1=0
sum_2=0
sum_3=0
sum_4=0
sum_5=0
sum_6=0

num_pause=0

prev_name="0"
prev_short_name="0"
prev_left="0"
prev_right="0"
prev_speaker="0"
prev_start="0"
prev_end="0"

while read name_file start end prediction; do
# while read name_file; do
# while read line; do
	# name_file=`echo ${line} | cut -d ' ' -f1`
	# prediction=`echo ${line} | cut -d ' ' -f2`
	name_file=${name_file%.*}
	short_name=`echo ${name_file} | cut -d '.' -f1,2`

	left=`echo ${name_file} | cut -d '.' -f2 | cut -d '-' -f1`
	right=`echo ${name_file} | cut -d '.' -f2 | cut -d '-' -f2`

	speaker=`echo ${name_file} | cut -d '.' -f3 | cut -d '_' -f1`

	
	# start=`echo ${name_file} | cut -d '_' -f2`
	# end=`echo ${name_file} | cut -d '_' -f3`
	start=$(echo ${start} | bc -l)
	end=$(echo ${end} | bc -l)

	# echo "sum click= ${sum_clicks}"
	# echo "sum bre= ${sum_bre}"


	if [[ "$short_name" != *$prev_name* ]]; then
		num_pause=0
	fi
	if (( $(echo "$temp_start != $zero" | bc -l) )); then
		if (( $(echo "$start != $temp_start" | bc -l) ))
			then
			num_pause=`echo "${num_pause}+1" | bc -l`
			echo "${num_pause},${prev_short_name},${prev_left}-${prev_right},${prev_speaker},${prev_start},${prev_end},,${sum_clicks},,${sum_bre}" >> ${output_file}
			echo "PRINT"
			sum_clicks=0
			sum_bre=0
		fi
	fi

	



	temp_start=$(echo ${start} | bc -l)

	prev_name="$(echo ${left}-${right})"

	prev_short_name="$(echo ${short_name})"
	prev_left="$(echo ${left})"
	prev_right="$(echo ${right})"
	prev_speaker="$(echo ${speaker})"
	prev_start="$(echo ${start})"
	prev_end="$(echo ${end})"

	echo "name : ${name_file}"

	# echo "prediction : ${prediction}"
	silences="silences"
	breathing="breathing"
	clicks="clicks"

	# cluster0="0"
	# cluster1="1"
	# cluster2="2"




	# awk -F"," 'BEGIN { OFS = "," } {$6="2012-02-29 16:13:00"; print}' input.csv > output.csv

	if [[ "$prediction" == sil* ]]; then
		prev_click=false
		prev_bre=false
	fi
	if [[ "$prediction" == 0* ]]; then
		if [ "$prev_bre" = false ]; then
			sum_bre=`echo "${sum_bre}+1" | bc -l`
			prev_bre=true
			prev_click=false
		fi
	fi
	if [[ "$prediction" == 3* ]]; then
		if [ "$prev_bre" = false ]; then
			sum_bre=`echo "${sum_bre}+1" | bc -l`
			prev_bre=true
			prev_click=false
		fi
	fi
	if [[ "$prediction" == 4* ]]; then
		if [ "$prev_click" = false ]; then
			sum_clicks=`echo "${sum_clicks}+1" | bc -l`
			prev_click=true
			prev_bre=false
		fi
	fi


	# if [[ $prediction == 0* ]]; then
	# 	sum_0=`echo "${sum_0}+1" | bc -l`
	# fi
	# # if [[ $prediction == 1* ]]; then
	# # 	sum_1=`echo "${sum_1}+1" | bc -l`
	# # fi
	# if [[ $prediction == 2* ]]; then
	# 	sum_2=`echo "${sum_2}+1" | bc -l`
	# fi
	# # if [[ $prediction == 3* ]]; then
	# # 	sum_3=`echo "${sum_3}+1" | bc -l`
	# # fi
	# # if [[ $prediction == 4* ]]; then
	# # 	sum_4=`echo "${sum_4}+1" | bc -l`
	# # fi
	# # if [[ $prediction == 5* ]]; then
	# # 	sum_5=`echo "${sum_5}+1" | bc -l`
	# # fi
	# # if [[ $prediction == 6* ]]; then
	# # 	sum_6=`echo "${sum_6}+1" | bc -l`
	# # fi

	# unsup
	# sum_clicks=`echo "${sum_2}" | bc -l`
	# sum_bre=`echo "${sum_0}" | bc -l`




done < file2.txt