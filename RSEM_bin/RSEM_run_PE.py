################################################################
#RSEM_run_PE.py										    14.12.05 -> 14.12.16
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

ref_dir = '/data/project/Mouse_network/hurben/ref_data/bowtie2_ref_genome/mm10_rsem_refseq'
rsem_dir = '/data/project/Mouse_network/hurben/packages/rsem/rsem-1.2.19/rsem-calculate-expression'
bowtie2_dir = '/data/project/Mouse_network/hurben/packages/bowtie2/bowtie2-2.2.4'


for i in range(len(fastq_list_readlines)):
	read = fastq_list_readlines[i]
	read = read.replace('\n','')

	
	file_token = read.split('\t')

	file_name_1 = file_token[0]
	file_name_2 = file_token[1]
	output_name = str(file_name_1) + '_'+ str(file_name_2) + '.rsem'


	print '################################'
	print '#Process step\t', output_name
	print '################################'

	rsem_cmd = str(rsem_dir) + ' -p 4 --bowtie2 --bowtie2-path ' + str(bowtie2_dir) + ' --paired-end ' + str(file_name_1) + ' ' + str(file_name_2) + ' ' + str(ref_dir) + ' ' + str(output_name)
	os.system(rsem_cmd)



#DONE









