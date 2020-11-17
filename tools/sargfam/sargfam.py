import os
import sys
import subprocess

input1 = sys.argv[1]
output1 = sys.argv[2]

# Step1 sum up in each file
commandstr="/home/xianmao/argoap_20.05/galaxy/tools/sargfam/hmmer-3.1b1/bin/hmmscan --cut_ga --tblout " + output1 + " --cpu 1 /home/xianmao/argoap_20.05/galaxy/tools/sargfam/DB/Sargfam.hmm " + input1 
print(commandstr)
command = commandstr.split(" ")
subprocess.Popen(command, cwd="/home/xianmao/argoap_20.05/galaxy/tools/sargfam/hmmer-3.1b1/bin")

