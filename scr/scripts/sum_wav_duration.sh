#!/bin/bash

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

if [ $# -ne 1 ] 
   then echo "${red}Enter the path of the directory with the .wav files${reset}"
   		read path_wav
else
    path_wav=$1 
    echo ${path_wav};
fi

wav_files=`find ${path_wav} -maxdepth 1 -name "*.wav"`

sum=0
nbr=0

for line in $wav_files ; do
	temp=`soxi -D ${line}`
	sum=`echo "${sum}+${temp}" | bc -l`
	nbr=`echo "${nbr}+1" | bc -l`
done

echo "${sum} seconds in ${nbr} files"
sum=`echo ${sum} | cut -d '.' -f1`
printf '%dd:%dh:%dm:%ds\n' $(($sum/86400)) $(($sum%86400/3600)) $(($sum%3600/60)) \
  $(($sum%60))