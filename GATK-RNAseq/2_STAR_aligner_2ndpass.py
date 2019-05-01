#----------------------------------------------------
#2_STAR_aligner_2ndpass.py					15.04.13
#
#
#
#STAR ALIGNER 2nd pass
#details: https://www.broadinstitute.org/gatk/guide/article?id=3891
#
#
#
#cmd : python 2_STAR_aligner_2ndpass.py [NEW genome DIR] [GENOME dir] [fragment size of fastq - 1]
#-----------------------------------------------------


#Genome building phase


import os
import sys


genome_dir = sys.argv[1]
genome_file = sys.argv[2]
size = sys.argv[3]
pass_dir = sys.argv[4]


#genome_dir = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF/readlength50_refseq'
#genome_file = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF/readlength50_refseq/mmu10_refseq.fa'
star_file ='//data/project/CAFFGENE_EXTENDED/packages/STAR-STAR_2.4.0k/source/STAR'



cmd = str(star_file) +' --runThreadN 8 --runMode genomeGenerate --genomeDir ' + str(genome_dir) + ' --genomeFastaFiles ' +str(genome_file) +' --sjdbFileChrStartEnd ' + str(pass_dir) + ' --sjdbOverhang ' + str(size)
print cmd

os.system(cmd)


