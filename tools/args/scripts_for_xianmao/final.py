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
                    type=str, default='.orf',metavar='.orf')

################################################## Definition ########################################################
args = parser.parse_args()
input_path = os.path.abspath(args.i)
list_data = glob.glob(os.path.join(input_path,'*'+args.f))
search_path = args.i + '/output'
# record preparation process
################################################### Programme #######################################################

# check the format of ORF, genbank parsing or prodigal prediction
orf_name=open(args.i + '/output/final.out','w')
a=0
for file_name in list_data:
    # check orf file
    filedir, file_name = os.path.split(file_name)
    for line in open(os.path.join(filedir,file_name)):
            if ( int(str(line).strip())%2 == 0):
                 orf_name.write(file_name+"\t"+str(line).strip()+"\n")
orf_name.close()
