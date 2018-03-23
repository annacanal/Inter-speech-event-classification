#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

if [ $# -ne 4 ] 
   then echo "${red}Enter the path of the directory with the .wav files${reset}"
   		read path_wav 
   		echo "${red}Enter the path of the directory with the temporary .txt files${reset}"
   		read path_txt
   		echo "${red}Enter the path of the directory for the output temporary .wav files${reset}"
   		read path_output 
   		echo "${red}Enter the path of the directory for the output .csv files with the extracted features${reset}"
   		read path_output_csv 
else
    path_wav=$1 
    echo ${path_wav};
    path_txt=$2 
    echo ${path_txt};
    path_output=$3 
    echo ${path_output};
    path_output_csv=$4 
    echo ${path_output_csv};
fi

# 1) Extract the non-speech segment and save them into dir
# wav_files=`find ${path_wav} -maxdepth 1 -name "*.wav"`

wav_files=`find ${path_wav} -maxdepth 1 -name "keynote*.wav"`
echo $wav_files;
rm todo.sh
for line in $wav_files ; do
	echo "$line"

	file_name=$(basename $line)
	file_name_witout_ext=${file_name%.*}

	python clicks_pauses_textgridtools.py ${file_name_witout_ext}.TextGrid
	#echo -e "$file_name_witout_ext"

	silence_file=`find ${path_txt} -maxdepth 1 -name "${file_name_witout_ext}_silences.txt"`
	breathing_file=`find ${path_txt} -maxdepth 1 -name "${file_name_witout_ext}_breathing.txt"`
	click_file=`find ${path_txt} -maxdepth 1 -name "${file_name_witout_ext}_clicks.txt"`


	while read begin end text; do
		begin=$(echo $begin | bc)
		end=$(echo $end | bc)
		echo "New silence ${begin} to ${end}"
		echo "ffmpeg -i ${line} -ss ${begin} -to ${end} -c copy ${path_output}/${file_name_witout_ext}_silences_${begin}_${end}.wav" >> todo.sh
	done < ${silence_file}

	echo "${blue}---------------${reset}"

	while read begin end text; do
		begin=$(echo $begin | bc)
		end=$(echo $end | bc)
		echo "New breathing ${begin} to ${end}"
		echo "ffmpeg -i ${line} -ss ${begin} -to ${end} -c copy ${path_output}/${file_name_witout_ext}_breathing_${begin}_${end}.wav" >> todo.sh
	done < ${breathing_file}

	echo "${blue}---------------${reset}"

	while read begin end text; do
		begin=$(echo $begin | bc)
		end=$(echo $end | bc)
		echo "New click ${begin} to ${end}"
		echo "ffmpeg -i ${line} -ss ${begin} -to ${end} -c copy ${path_output}/${file_name_witout_ext}_clicks_${begin}_${end}.wav" >> todo.sh
	done < ${click_file}

	echo "${blue}---------------${reset}"
done

bash todo.sh
rm todo.sh

# silence_wav_files=`find ${path_output} -maxdepth 1 -name "${file_name_witout_ext}*.wav"`
silence_wav_files=`find ${path_output} -maxdepth 1 -name "*.wav"`

for sil_line in $silence_wav_files ; do
	bash extract_features.sh ${sil_line} ${path_output_csv}
done

rm ${path_output_csv}/list.txt
ls ${path_output_csv}/ > ${path_output_csv}/list.txt