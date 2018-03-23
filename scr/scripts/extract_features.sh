#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

if [ $# -ne 3 ] 
   then echo "${red}Enter the path of the .wav silence file ${reset}"
   		read path_wav
   		echo "${red}Enter the path of the desired output directory for the .csv file${reset}"
   		read path_csv
   		echo "${red}Enter the path of the directory of your openSMILE distribution (needs to end by /inst/bin )${reset}"
   		read path_open
else
    path_wav=$1 
    path_csv=$2
    path_open=$3
fi

echo "${blue}File : ${path_wav}${reset}";
echo "${blue}Saved in : ${path_csv}${reset}";

file_name=$(basename $path_wav)
file_name_witout_ext=${file_name%.*}


# /Users/Marine/Downloads/openSMILE-2.1.0/inst/bin/SMILExtract  -C IS09_emotion.conf  -I ${path_wav}  -O ${path_csv}/${file_name_witout_ext}_1.csv
${path_open}/SMILExtract  -C config/IS09_emotion_Final.conf  -I ${path_wav}  -O ${path_csv}/${file_name_witout_ext}.csv