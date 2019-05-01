#----------------------------------------------------
#1_STAR_aligner_1stpass.py					15.04.13
#
#
#description : STAR 1stpass phase. must use after genome build.
#details : https://www.broadinstitute.org/gatk/guide/article?id=3891
#
#AFTER this. must use 2_STAR_aligner_2ndpass.py
#
#
#cmd python #1_STAR_aligner_1stpass.py [fq.list]
#-----------------------------------------------------

#CAUTION
#FOR NON-PAIR END DATA
#LIST INPUT
#path/file_1.fastq[tab]path/file_2.fastq




import os
import sys


file_with_dir = sys.argv[1]

second_pass_ref_dir = sys.argv[2]


ref_file = '//data/project/CAFFGENE_EXTENDED/data/ref_data/mmu10_refseq.fa'
star_file ='//data/project/CAFFGENE_EXTENDED/packages/STAR-STAR_2.4.0k/source/STAR'




cmd = str(star_file) +' --runThreadN 8 --genomeDir ' + str(second_pass_ref_dir) + ' --readFilesIn ' +str(file_with_dir)

os.system(cmd)

