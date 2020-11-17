import os
import sys
import subprocess

input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]
input4 = sys.argv[4]
output1 = sys.argv[5]
output2 = sys.argv[6]

# Step1 sum up in each file
commandstr="bash /home/xianmao/argoap_20.05/galaxy/tools/MST/script.sh " + input1 + " " + input2 + " " + input3 + " " + input4 + " " + output1 + " " + output2
print(commandstr)
command = commandstr.split(" ")
subprocess.Popen(command, cwd="/home/xianmao/argoap_20.05/galaxy/tools/MST")
