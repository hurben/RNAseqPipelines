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


seq_list_argv = sys.argv[1]
seq_list_file = file(seq_list_argv)
seq_list_readlines = seq_list_file.readlines()

star_file ='//data/project/CAFFGENE_EXTENDED/packages/STAR-STAR_2.4.0k/source/STAR'

genome_dir = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF'
genome_file = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF/mmu10_refseq.fa'
gtf_file = '//data/project/CAFFGENE_EXTENDED/data/ref_data/mmu10.gtf'



for i in range(len(seq_list_readlines)):
	read = seq_list_readlines[i]
	read = read.replace('\n','')

	file_with_dir = read
	token = read.split('/')
	file_name = token[len(token) -1]
	out_name = str(file_name)+'.1st_pass'

	cmd = 'mkdir ' + str(out_name)
	os.system(cmd)

	cmd = str(star_file) +' --runThreadN 8 --genomeDir ' + str(genome_dir) + ' --readFilesIn ' +str(file_with_dir) + ' --outFileNamePrefix ./' +str(out_name)

	os.system(cmd)

