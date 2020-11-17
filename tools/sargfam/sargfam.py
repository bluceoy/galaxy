import os
import argparse
import glob
import copy


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i",
                    help="input file",
                    type=str, default='input',metavar='input1')
parser.add_argument("-o",
                    help="output file",
                    type=str, default='output.txt',metavar='output.txt')

args = parser.parse_args()
input1 = os.path.abspath(args.i)
input_dir = os.path.dirname(args.i) 
workingdir = os.path.abspath(os.path.dirname(__file__))
output_dir = input_dir + '/output'
try:
    os.mkdir(output_dir)
except OSError:
    pass

# Step1 sum up in each file
cmd="/home/xianmao/argoap_20.05/galaxy/tools/sargfam/hmmer-3.1b1/bin/hmmscan --cut_ga --tblout "+output_dir+"/final.txt --cpu 1 /home/xianmao/argoap_20.05/galaxy/tools/sargfam/DB/Sargfam.hmm "+input1
print(cmd)
os.system(cmd)
