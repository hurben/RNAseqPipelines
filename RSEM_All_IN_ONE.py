################################################################
#RSEM_All_IN_ONE.py									    15.04.17
#Process for doing RSEM + After RSEM 
#
#description : [1] Aligning raw fasta.q files (RNA-seq)
#              [2] Refseq process must be done
#                  
#IMPORANT NOTE  [2-1]rsem-prepare-reference MUST BE DONE BEFORE THIS PROGRAM
#
#
#INPUT : FASTQ.list ( trimmed)
#OUTPUT : FPKM matrix
#
#
#################################################################
#[list of fastq] format
#"PATH/filename"
#each sample per line

def Read_files_from_lists(list_of_files_argv):
#Important Note:
#About INPUT:
#list of files must have a format of
#/file_name_1\n
#/file_name_2\n
#/file_name_3\n
#...
#...
	dict = {}
	sample_list = []
	transcript_list = []

	list_file_open = file(list_of_files_argv)
	list_file_readlines = list_file_open.readlines()

	#Read Path+file name from "sample list"
	for i in range(len(list_file_readlines)):
		read = list_file_readlines[i]
		read = read.replace('\n','')

		file_name = read.split('/')[len(read.split('/'))-1]
		file_name = file_name.split('.')[0]
		print file_name

		single_file_data = read

		#Using Read_single_file function. (Function is included in the same library)
		transcript_tmp = Read_single_file(single_file_data,file_name,dict)
		#transcript_tmp is "list" of transcript ids generated by RSEM.
		#transcript id are in UCSC format in my case.
		
		#Check whether the readed file is duplicated or not.
		if file_name in sample_list: #For duplicated sample checking
			print '####### WARNING #######'
			print read
			print file_name, ' duplicated'
			print '#######################'
		if file_name not in sample_list:
			sample_list.append(file_name)

		for transcript_id in transcript_tmp:
			transcript_list.append(transcript_id)
	


	transcript_set_list = set(list(transcript_list))


	return dict, sample_list, transcript_set_list



def Read_single_file(single_file_data,file_name,dict):
#CAUTION : ONLY FOR RSEM RESULTS
	
	number_of_0_fpkm = 0

	transcript_id_list = []
	
	single_file_open = file(single_file_data)
	single_file_readlines = single_file_open.readlines()

	for i in range(1, len(single_file_readlines)):
		read = single_file_readlines[i]
		read = read.replace('\n','')

		transcript_id = read.split('\t')[1]
		transcript_id_list.append(transcript_id)
		fpkm = read.split('\t')[6]
		Make_dict(transcript_id,fpkm,dict,file_name)

		if float(fpkm) == 0.00:
			number_of_0_fpkm += 1


	print file_name, ' : ', number_of_0_fpkm, 'genes recorded as FPKM 0'
	
	transcript_id_set_list = set(list(transcript_id_list))

	return transcript_id_set_list

			

def Make_dict(transcript_id,fpkm,dict,file_name):
	dict[transcript_id,file_name] = fpkm



def Make_dict_as_matrix_text(dict,sample_list,text,transcript_list):
#Important Note:
#dict[key] = [[A,B],[A,B],[A,B] ... ]
#key = transcript id
#A = FPKM
#B = sample id

#for matrix text format
#
	print 'Total samples', len(sample_list)
	print 'Total transcript ids', len(transcript_list)

	result_text = file(str(text),'w')
	
	#Writing header for text
	result_text.write('gene')
	for sample_id in sample_list:
		result_text.write('\t' + str(sample_id))
	result_text.write('\n')
	
	for transcript_id in transcript_list:
		result_text.write(str(transcript_id))
		for sample_id in sample_list:
			fpkm = dict[transcript_id, sample_id]
			result_text.write('\t' + str(fpkm))
		result_text.write('\n')



import os
import sys

#input. list of fastq files
fastq_list_argv = sys.argv[1]
fastq_list_file = file(fastq_list_argv)
fastq_list_readlines = fastq_list_file.readlines()


#Package/ essential file declare
ref_dir = '//data/project/CAFFGENE_EXTENDED/data/ref_data/mm10_rsem_refseq'
rsem_dir = '//data/project/CAFFGENE_EXTENDED/packages/rsem-1.2.19/rsem-calculate-expression'
bowtie2_dir = '//data/project/CAFFGENE_EXTENDED/packages/bowtie2-2.2.4'
ucsc_converter_info = '//data/project/CAFFGENE_EXTENDED/data/ref_data/mm10_kgXref'



#Read FASTQ FILE LIST
for i in range(len(fastq_list_readlines)):
	read = fastq_list_readlines[i]
	read = read.replace('\n','')

	token = read.split('/')
	
	#Declaring Folder. Results will be saved in the master folder.
	master_folder = token[len(token)-2]

	print "Starting & Saved in : ", master_folder
	print '---- RSEM Alignment ----'

	file_dir = read
	file_name = token[len(token)-1].split('.')[0]
	output_name = str(file_name) + '.rsem'

	print '#Process step : ', file_name

	output_dir_with_file = './' + str(master_folder) + '/' + str(output_name)
	print output_dir_with_file

	#CREATE Directory : master folder
	mkdir_master_folder = 'mkdir ' + str(master_folder)
	os.system(mkdir_master_folder)


	#RUN RSEM
	rsem_cmd = str(rsem_dir) + ' -p 8 --bowtie2 --bowtie2-path ' + str(bowtie2_dir) + ' ' + str(file_dir) + ' ' + str(ref_dir) + ' ' + str(output_dir_with_file)
	print rsem_cmd
	os.system(rsem_cmd)


#AFTER ALL RSEM ALIGNMENT IS COMPLETED, MAKE INTEGRATED MATRIX

print "RSEM Alignment DONE : ", str(fastq_list_argv)
print "Proceeding FPKM to matrix"

cmd = "ls ./" + str(master_folder)+'/*.rsem.genes* > ./' +str(master_folder)+ '/gene.list'
print cmd
os.system(cmd)

gene_list_argv = './' + str(master_folder) + '/gene.list'
gene_list_file = file(gene_list_argv)
gene_list_readlines = gene_list_file.readlines()

fpkm_dict = {}

#fpkm_matrix_text = 'temp.txt'
fpkm_matrix_text = './' + str(master_folder) + '/' +str(master_folder)+'.fpkm.matrix'

#Function
fpkm_dict, sample_list, transcript_list = Read_files_from_lists(gene_list_argv)

Make_dict_as_matrix_text(fpkm_dict,sample_list,fpkm_matrix_text,transcript_list)

#FPKM_MATRIX_GENERATION DONE


ucsc_output = './' + str(master_folder) +'.fpkm.genesymbol.matrix'
print ucsc_output

ucsc_converting_cmd = 'python //data/project/CAFFGENE_EXTENDED/bin/After_RSEM/UCSC_geneID_to_official_gene_symbol.py ' + str(fpkm_matrix_text) + ' ' +str(ucsc_converter_info) + ' ' + str(ucsc_output)
os.system(ucsc_converting_cmd)












