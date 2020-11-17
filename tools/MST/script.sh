#!/bin/bash


email_2=`echo ${3}| sed 's/@/at/g'`
locltime=`date| sed 's/ /_/g'|sed 's/:/_/g' `

Rscript /home/lg209ws3/argoap_18.05/galaxy/tools/MST/scripts_ARGs-OAP.R ${1}

cp ${1}.source_proportions.txt /home/lg209ws3/argoap_18.05/galaxy/USEROUTPUTmst/${2}_${email_2}_${4}_${locltime}.source_proportions.txt
cp ${1}.source_proportions_sd.txt /home/lg209ws3/argoap_18.05/galaxy/USEROUTPUTmst/${2}_${email_2}_${4}_${locltime}.source_proportions_sd.txt

cp ${1}.source_proportions.txt ${5}
cp ${1}.source_proportions_sd.txt ${6}
