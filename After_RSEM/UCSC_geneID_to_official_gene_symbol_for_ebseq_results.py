##################################################################
#UCSC_geneID_to_official_gene_symbol.py					15.01.14
#
#
#
#Description : [1] Read matrix from resulted file.
#			   [2] Just change KEY to GENE SYMBOL
#
#command line : UCSC_geneID_to_official_gene_symbol.py [matrix.dat] [converter info] [output]
#################################################################
#Important note
#Matrix file format : column = sample, row[0] = gene, row[n+1] = FPKM




#starting Program : UCSC_geneID_to_official_gene_symbol.py

if __name__ == '__main__':


	import sys
	import argparse
	import subprocess
	import os

	#location of bin folder : in other words, the program location
	program_dir = os.path.split(os.path.realpath(__file__))

	#call library path & function : error_check
	lib_path = os.path.abspath(str(program_dir[0])+'/')
	import Matrix_Process_FL

	matrix_dat = sys.argv[1]
	converter_info = sys.argv[2]
	result_list_data = sys.argv[3]
	result_text = sys.argv[4]

	txt = file(result_text, 'w')

    #create dictionary from a single matrix data
	matrix_dict, sample_list = Matrix_Process_FL.READ_RSEM_MATRIX_DATA(matrix_dat)
	#KEY = SOMEKIND OF ID


	converter_info_dict = Matrix_Process_FL.READ_MATRIX_REFFLAT(converter_info)


	result_list_data_open = file(result_list_data)
	result_list_data_readlines = result_list_data_open.readlines()

	for i in range(len(result_list_data_readlines)):
		read = result_list_data_readlines[i]
		read = read.replace('\n','')
		
		read = read.replace('"','')

		if read in matrix_dict.keys():

			transcript_id = matrix_dict[read][0]
			gene = converter_info_dict[transcript_id]

			txt.write(str(gene) + '\n')

			
			
		


	





#DONE
