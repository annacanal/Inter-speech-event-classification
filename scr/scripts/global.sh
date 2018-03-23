#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

if [ $# -ne 4 ] 
   then echo "${red}Enter the path of the directory with the .wav files${reset}"
   		read path_wav 
   		echo "${red}Enter the path of the directory with the .words files${reset}"
   		read path_words
   		echo "${red}Enter the path of the directory for the output temporary .wav files${reset}"
   		read path_output 
   		echo "${red}Enter the path of the directory for the output .csv files with the extracted features${reset}"
   		read path_output_csv 
else
    path_wav=$1 
    echo ${path_wav};
    path_words=$2 
    echo ${path_words};
    path_output=$3 
    echo ${path_output};
    path_output_csv=$4 
    echo ${path_output_csv};
fi


wav_files=`find ${path_wav} -maxdepth 1 -name "*.wav"`
echo $wav_files;

for line in $wav_files ; do
	echo "$line"
	#look for the linked .words file
	file_name=$(basename $line)
	file_name_witout_ext=${file_name%.*}
	#echo -e "$file_name_witout_ext"
	words_file=`find ${path_words} -maxdepth 1 -name "${file_name_witout_ext}.words"`
	cat ${words_file} | grep -B1 "<P>" > silences_lines.txt
	#echo ${silences_lines};
	begin=$(echo "-1" | bc -l)
	end=0
	zero=0
	while read -r f1 f2 f3 f4 f5 f6 f7; do

		if [ "$f1" = "--" ]
			then
				echo "New silence ${begin} to ${end}"
				echo "ffmpeg -i ${line} -ss ${begin} -to ${end} -c copy ${path_output}/${file_name_witout_ext}_${begin}_${end}.wav" >> todo.sh
				begin=$(echo "-1" | bc -l)
				end=0
		else
			if (( $(echo "$begin < $zero" | bc -l) ))
				then 
					if  [ "$f1" = "#" ]
						then begin=0
					else
						begin=$(echo $f1 | bc | awk '{printf "%f", $0}')
					fi
			else
				if (( $(echo "$end <= $zero" | bc -l) ))
					then end=$(echo $f1 | bc)
				else
					echo "New silence ${begin} to ${end}"
					echo "ffmpeg -i ${line} -ss ${begin} -to ${end} -c copy ${path_output}/${file_name_witout_ext}_${begin}_${end}.wav" >> todo.sh
					begin=$(echo $end | bc)
					end=$(echo $f1 | bc)
				fi
			fi
		fi

	done <silences_lines.txt
	
	bash todo.sh
	rm silences_lines.txt
	rm todo.sh
done

# silence_wav_files=`find ${path_output} -maxdepth 1 -name "${file_name_witout_ext}*.wav"`
silence_wav_files=`find ${path_output} -maxdepth 1 -name "*.wav"`
	
	for sil_line in $silence_wav_files ; do
		bash extract_features.sh ${sil_line} ${path_output_csv}
	done

rm ${path_output_csv}/list.txt
ls ${path_output_csv}/ > ${path_output_csv}/list.txt
