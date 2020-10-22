import os
import argparse
import glob
import copy


############################################ Arguments and declarations ##############################################
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i",
                    help="input directory or folder of your sequences",
                    type=str, default='input',metavar='input')
parser.add_argument("-f",
                    help="file type or filename extension of your sequences.\n \
                         To input genbank file, set \"-f .gbff\" or \"-f .gbff.gz\"",
                    type=str, default='.fa',metavar='.fa, .fasta, .fna, .gbff, .gbff.gz')

################################################## Definition ########################################################
args = parser.parse_args()
in_dir= os.path.abspath(args.i)
workingdir = os.path.abspath(os.path.dirname(__file__))
input_extension = args.f
list_data = glob.glob(os.path.join(in_dir,'*'+input_extension))
search_path = in_dir + '/output'
try:
    os.mkdir(search_path)
except OSError:
    pass

################################################### Programme #######################################################
# Step1 sum up in each file
cmd1 = 'python '+workingdir+'/scripts_for_xianmao/Preparation.py -i ' + str(in_dir) + ' -f ' + str(input_extension) +' \n'
os.system(cmd1)
# Step2 remainer if divided by two
cmd2 = 'python '+workingdir+'/scripts_for_xianmao/final.py -i ' + str(in_dir) + ' -f .orf'  +' \n'
os.system(cmd2)
