#########################################################
#fpkm_check_and_matrix_maker.py								14.12.26
#
#
#Description : [1] Read matrix list from "list file" -> in function library
#              [2] Read RSEM result file "genes.results"
#			       1) count number of genes that have " FPKM > 0 "
#				   2) save dict['transcript_id'] = [[fpkm,sample#],[fpkem,sample#] ... ]
#					-> maybe exclude extreme fpkm samples.
#			   [3] OUTPUT
#			  	   1) matrix file
#				   2) and more?
#
#command line : fpkm_check_and_matrix_maker.py [list of genes] [output name]
##########################################################
#Important Note:
#About INPUT:
#list of files must have a format of
#path/file_name_1\n
#path/file_name_2\n
#path/file_name_3\n
#...
#...


#starting Program : fpkm_check_and_matrix_maker.py

if __name__ == '__main__':


	import sys
	import argparse
	import subprocess
	import os

	#location of bin folder : in other words, the program location
	program_dir = os.path.split(os.path.realpath(__file__)) 

	#call library path & function : error_check
	lib_path = os.path.abspath(str(program_dir[0])+'/')
	import Function_library

	list_of_files = sys.argv[1]
	output_file = sys.argv[2]

	#READ data from list & read single file & making dictionary
	dict, sample_list, transcript_list = Function_library.Read_files_from_lists_ver_fpkm(list_of_files)

	uniq_sample_list = list(set(sample_list))


	print 'Total considered samples ', len(sample_list)
	print 'Total unique samples ', len(uniq_sample_list)

	#make matrix & output file
	Function_library.Make_dict_as_matrix_text(dict,uniq_sample_list,output_file, transcript_list)
	


