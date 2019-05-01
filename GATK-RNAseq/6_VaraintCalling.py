import sys
import os

sam_list = sys.argv[1]
sam_list_file = file(sam_list)
sam_list_readlines = sam_list_file.readlines()


picard_dir = '//data/project/CAFFGENE_EXTENDED/packages/picard/picard-tools-1.115/'
gatk_package = '//data/project/CAFFGENE_EXTENDED/packages/GenomeAnalysisTK.jar'
ref_seq = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF/mmu10_refseq.fa'


for i in range(len(sam_list_readlines)):
	read = sam_list_readlines[i]
	read = read.replace('\n','')
	token = read.split('/')
	input_file = token[len(token) -1]
	folder_name = token[len(token) -2]
	output_name = str(folder_name) + '.vcf'

	mkdir_cmd = 'mkdir ' + str(folder_name)
	os.system(mkdir_cmd)

	

	cmd = 'java -jar ' + str(gatk_package) +' -T HaplotypeCaller -R ' +str(ref_seq) + ' -I ' +str(read) + ' -o ./' +str(folder_name) +'/' + str(output_name) + ' -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS'
#	cmd = 'java -jar ' + str(gatk_package) +' -T SplitNCigarReads -R ' +str(ref_seq) + ' -I ' +str(read) + ' -o test.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS'
	print cmd
	os.system(cmd)
