################################################################
#RSEM_run.py										    14.12.05
#
#
#description : [1] Aligning raw fasta.q files (RNA-seq)
#              [2] Refseq process must be done
#                  
#              [2-1]rsem-prepare-reference MUST BE DONE BEFORE THIS PROGRAM
#
#
#
#python RSEM_run.py [list of fastq] 
#################################################################
#[list of fastq] format
#"PATH/filename"
#each sample per line


import os
import sys

#input. list of fastq files
fastq_list_argv = sys.argv[1]
fastq_list_file = file(fastq_list_argv)
fastq_list_readlines = fastq_list_file.readlines()

ref_dir = '//data/project/CAFFGENE_EXTENDED/data/ref_data/mm10_rsem_refseq'
rsem_dir = '//data/project/CAFFGENE_EXTENDED/packages/rsem-1.2.19/rsem-calculate-expression'
bowtie2_dir = '//data/project/CAFFGENE_EXTENDED/packages/bowtie2-2.2.4'


for i in range(len(fastq_list_readlines)):
	read = fastq_list_readlines[i]
	read = read.replace('\n','')

	
	token = read.split('/')

	file_dir = read
	file_name = token[len(token)-1].split('.')[0]
	output_name = str(file_name) + '.rsem'

	print '################################'
	print '#Process step\t', file_name
	print '################################'

	rsem_cmd = str(rsem_dir) + ' -p 8 --output-genome-bam --bowtie2 --bowtie2-path ' + str(bowtie2_dir) + ' ' + str(file_dir) + ' ' + str(ref_dir) + ' ' + str(output_name)
	print rsem_cmd
	os.system(rsem_cmd)



#DONE









