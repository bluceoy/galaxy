import os
import argparse
import glob


############################################ Arguments and declarations ##############################################
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i",
                    help="input directory or folder of your sequences",
                    type=str, default='input',metavar='input')
parser.add_argument("-f",
                    help="file type or filename extension of your sequences",
                    type=str, default='.fa',metavar='.fa or .fasta or .fna')

################################################## Definition ########################################################
args = parser.parse_args()
input_path = os.path.abspath(args.i)
list_data = glob.glob(os.path.join(input_path,'*'+args.f))
search_path = args.i + '/output'
# record preparation process

################################################### Programme #######################################################
# check the format of ORF, genbank parsing or prodigal prediction
fot=open(args.i + '/output/ORF_format.log','w')
a=0
for file_name in list_data:
    # check orf file
    filedir, file_name = os.path.split(file_name)
    orf_name=file_name.replace(args.f,".orf")
    f1 = open(os.path.join(filedir,orf_name),'w')
    for line in open(os.path.join(filedir,file_name)):
            a=a+int(line.strip())
    f1.write(str(a)+'\n')
    f1.close()
