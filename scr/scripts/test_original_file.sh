#!/bin/bash

rm test_file.sh


if [ $# -ne 1 ] 
   then echo "${red}Enter the path of the .wav cutted file ${reset}"
   		read path_wav
else
    path_wav=$1 
    # echo "${blue}File : ${path_wav}${reset}";
fi


silence_wav_files=`find ${path_wav} -maxdepth 1 -name "*silence*.wav"`

for sil_line in $silence_wav_files ; do
	echo "ffplay ${sil_line} -nodisp -autoexit" >> test_file.sh
done


bash test_file.sh
rm test_file.sh