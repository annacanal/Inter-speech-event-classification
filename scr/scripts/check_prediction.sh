#!/bin/bash


red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`


if [ $# -ne 2 ] 
   then echo "${red}Enter the path of the file with the prediction${reset}"
   		read path_prediction 
   		echo "${red}Enter the path of the directory with the cutted .wav files${reset}"
   		read path_wav
else
    path_prediction=$1 
    echo ${path_prediction};
    path_wav=$2 
    echo ${path_wav};
fi


cat ${path_prediction} | cut -d ',' -f2,5 > file.txt

cat file.txt | sed s/','/'\ '/g > file2.txt


rm silences.sh
rm breathing.sh
rm clicks.sh
rm cluster0.sh
rm cluster1.sh
rm cluster2.sh

while read name_file prediction; do
# while read line; do
	# name_file=`echo ${line} | cut -d ' ' -f1`
	# prediction=`echo ${line} | cut -d ' ' -f2`
	name_file=${name_file%.*}
	echo "name : ${name_file}"
	echo "prediction : ${prediction}"
	silences="silences"
	breathing="breathing"
	clicks="clicks"

	cluster0="0"
	cluster1="1"
	cluster2="2"

	echo "--${prediction}--"
	echo "--${cluster0}--"


	if [[ "$prediction" == sil* ]]; then
		echo "ffplay ${path_wav}/${name_file}.wav -nodisp -autoexit" >> silences.sh
		echo "oks"
	fi
	if [[ "$prediction" == breath* ]]; then
		echo "ffplay ${path_wav}/${name_file}.wav -nodisp -autoexit" >> breathing.sh
		echo "okb"
	fi
	if [[ "$prediction" == click* ]]; then
		echo "ffplay ${path_wav}/${name_file}.wav -nodisp -autoexit" >> clicks.sh
		echo "okc"
	fi


	if [[ $prediction == 0* ]]; then
		echo "ffplay ${path_wav}/${name_file}.wav -nodisp -autoexit" >> cluster0.sh
		echo "ok0"
	fi
	if [[ $prediction == 1* ]]; then
		echo "ffplay ${path_wav}/${name_file}.wav -nodisp -autoexit" >> cluster1.sh
		echo "ok1"
	fi
	if [[ $prediction == 2* ]]; then
		echo "ffplay ${path_wav}/${name_file}.wav -nodisp -autoexit" >> cluster2.sh
		echo "ok2"
	fi

done < file2.txt

echo "${red}BREATHING${reset}"
read -p "${red}BREATHING${reset}"
echo " ";

bash breathing.sh

echo "${red}CLICKS${reset}"
read -p "${red}CLICKS${reset}"

bash clicks.sh

echo "${red}SILENCES${reset}"
read -p "${red}SILENCES${reset}"

bash silences.sh


echo "${red}Cluster 0${reset}"
read -p "${red}Cluster 0${reset}"

bash cluster0.sh


echo "${red}Cluster 1${reset}"
read -p "${red}Cluster 1${reset}"

bash cluster1.sh

echo "${red}Cluster 2${reset}"
read -p "${red}Cluster 2${reset}"
echo " ";

bash cluster2.sh



