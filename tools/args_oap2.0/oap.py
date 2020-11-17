import os
import sys
import subprocess

input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]
input4 = sys.argv[4]
input5 = sys.argv[5]
input6 = sys.argv[6]
input7 = sys.argv[7]
input8 = sys.argv[8]
input9 = sys.argv[9]
output1 = sys.argv[10]
output2 = sys.argv[11]
output3 = sys.argv[12]
output4 = sys.argv[13]
output5 = sys.argv[14]

# Step1 sum up in each file
args = [input1, input2, input3, input4, input5, input6, input7, input8, input9, output1, output2, output3, output4, output5]
commandstr="/home/xianmao/argoap_20.05/galaxy/tools/args_oap2.0/ublastx_stage_two_version2.0.modify " + " ".join(args)
print(commandstr)
command = commandstr.split(" ")
subprocess.Popen(command, cwd="/home/xianmao/argoap_20.05/galaxy/tools/args_oap2.0")
