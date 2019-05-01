#######################################################
#FUNCTION LIBARARY 1.0.0  					   15.01.05
#######################################################

def Read_files_from_lists_ver_fpkm(list_of_files_argv):
#Important Note:
#About INPUT:
#list of files must have a format of
#path/file_name_1\n
#path/file_name_2\n
#path/file_name_3\n
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

		single_file_data = read

		#Using Read_single_file function. (Function is included in the same library)
		transcript_tmp = Read_single_file_ver_fpkm(single_file_data,file_name,dict)
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


def Read_files_from_lists_ver_count(list_of_files_argv):
#Important Note:
#About INPUT:
#list of files must have a format of
#path/file_name_1\n
#path/file_name_2\n
#path/file_name_3\n
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

		single_file_data = read

		#Using Read_single_file function. (Function is included in the same library)
		transcript_tmp = Read_single_file_ver_count(single_file_data,file_name,dict)
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




def Read_single_file_ver_count(single_file_data,file_name,dict):
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
		fpkm = read.split('\t')[4]
		Make_dict(transcript_id,fpkm,dict,file_name)

		if float(fpkm) == 0.00:
			number_of_0_fpkm += 1


	print file_name, ' : ', number_of_0_fpkm, 'genes recorded as expected_count 0'
	
	transcript_id_set_list = set(list(transcript_id_list))

	return transcript_id_set_list

	
def Read_single_file_ver_fpkm(single_file_data,file_name,dict):
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






		

