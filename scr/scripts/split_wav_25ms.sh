#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

if [ $# -ne 3 ] 
   then echo "${red}Enter the path of the directory with the .wav files you want to split${reset}"
   		read path_wav 
   		echo "${red}Enter the path of the directory for the output temporary .wav files${reset}"
   		read path_output 
   		echo "${red}Enter the path of the directory for the output .csv files with the extracted features${reset}"
   		read path_output_csv 
else
    path_wav=$1 
    echo ${path_wav};
    path_output=$2 
    echo ${path_output};
    path_output_csv=$3
    echo ${path_output_csv};
fi



# wav_files=`find ${path_wav} -maxdepth 1 -name "keynote-*.wav"`
wav_files=`find ${path_wav} -maxdepth 1 -name "*.wav"`
# echo $wav_files;


# SPLIT audio files into files of 25 ms
for line in $wav_files ; do
	echo -e "          $line"
	file_name=$(basename $line)
  	file_name_witout_ext=${file_name%.*}
	echo ${file_name_witout_ext}

	split_size=0.25
	echo ${split_size}

	sox "$line" ${path_output}/${file_name_witout_ext}_25ms.wav trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size} : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}  : newfile trim 0 ${split_size}

	echo " ";
done

## silence_wav_files=`find ${path_output} -maxdepth 1 -name "${file_name_witout_ext}*.wav"`
silence_wav_files=`find ${path_output} -maxdepth 1 -name "*_25ms*.wav"`
	
	for sil_line in $silence_wav_files ; do
		bash extract_features.sh ${sil_line} ${path_output_csv}
	done

rm ${path_output_csv}/list.txt
ls ${path_output_csv}/ > ${path_output_csv}/list.txt

