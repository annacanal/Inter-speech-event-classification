This file explains the roles of the scripts in the scripts/ folder


In order for this scripts to work you have ffmpeg (AND ffplay) installed as well as OpenSMILE and sox.

------------ case_study_global.sh ------------

This script will take as parameters:

- the path of the directory with the original .wav files of the case study.

- the path of the directory with the temporary .txt files
	Those files are used to extract the non-speech segments in the original .wav files. Those files can be deleted afterwards.

- the path of the directory for the output .wav files
	Those files are the extracted non-speech segments.

- the path of the directory for the output .csv files with the extracted features
	Those files are the extracted features.


It uses: clicks_pauses_textgridtools.py and extract_features.sh




------------ global.sh ------------

This script will take as parameters:

- the path of the directory with the original .wav files of GECO.

- the path of the directory with the temporary .words files
	Those files are used to extract the non-speech segments in the original .wav files. 

- the path of the directory for the output .wav files
	Those files are the extracted non-speech segments.

- the path of the directory for the output .csv files with the extracted features
	Those files are the extracted features.


It uses: extract_features.sh


------------ extract_features.sh ------------

This script will take as parameters:

- the path of the .wav silence file you want to extract features from.

- the path of the desired output directory for the .csv file.

- the path of the directory of your openSMILE distribution (needs to end by /inst/bin )

NB: You have to change the file if you want to change the configuration file for the extraction.
All the configuration files used are available in the config/ folder.




------------ check_prediction.sh ------------

This script will take as parameters:

- the path of the file with the predictions (timestamp_*).

- the path of the directory with the cutted .wav files.

What this script does is playing the .wav files one by one.
If the predicitons are labeled (supervised learning) : breathing, then clicks and then silences. (Tap "Enter" to continue between classes)
If the predicitons are not labeled (unsupervised learning) : cluster 0, then cluster 1 and then cluster 2. (Tap "Enter" to continue between clusters)

It uses: ffplay


------------ split_wav_25ms.sh ------------


This script will take as parameters:

- the path of the directory with the .wav files you want to split into 25 ms ones.

- the path of the directory for the output .wav files
	Those files are the extracted non-speech segments of 25ms.

- the path of the directory for the output .csv files with the extracted features
	Those files are the extracted features.


It uses: sox and extract_features.sh



------------ sum_wav_duration.sh ------------

This script will take as parameters:

- the path of the directory with the .wav files you want to have the sum of the duration of.

It uses: soxi


------------ test_orignal_file.sh ------------

This script will take as parameters:

- the path of the .wav cutted file from the case study.

This script will play the original segments that are labeled as silences in the case study.

It uses: ffplay


------------ evaluation.sh ------------

This script will take as parameters:

- the path of the .csv prediction file of the supervised algorithm tested on case study or GECO.

This script will write in a file the number of clicks and breathing detected in each pauses (to be compared to manual annotations)



------------ evaluation_2.sh ------------

This script will take as parameters:

- the path of the .csv prediction file of the unsupervised algorithm tested on case study or GECO.

This script will write in a file the number of clicks and breathing detected in each pauses (to be compared to manual annotations)

Observation: clusters with breathing and clicks needs to be identified and the script adpated accordingly.
