import sys
import os

sam_list = sys.argv[1]
sam_list_file = file(sam_list)
sam_list_readlines = sam_list_file.readlines()


picard_dir = '//data/project/CAFFGENE_EXTENDED/packages/picard/picard-tools-1.115/'


for i in range(len(sam_list_readlines)):
	read = sam_list_readlines[i]
	read = read.replace('\n','')
	token = read.split('/')
	output = token[len(token) -1]
	folder_name = token[len(token) -2]
	

	mkdir_cmd = 'mkdir ' + str(folder_name)
	os.system(mkdir_cmd)

	cmd = 'java -jar ' + str(picard_dir)+'AddOrReplaceReadGroups.jar I=' +str(read) + ' O=./'+str(folder_name) + '/' +str(output)+ ' SO=coordinate RGID=id RGLB=library RGPL=platform RGPU=machine RGSM=sample'
	os.system(cmd)
	print cmd

	second_output = str(output) + '.dedup'
	cmd = 'java -jar ' + str(picard_dir)+'MarkDuplicates.jar I=./'+str(folder_name)+'/' +str(output) + ' O=./'+str(folder_name) +'/' +str(second_output)+ '.bam CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=./'+str(folder_name) + '/' + str(second_output)+'.metrics'
	print cmd

	os.system(cmd)
