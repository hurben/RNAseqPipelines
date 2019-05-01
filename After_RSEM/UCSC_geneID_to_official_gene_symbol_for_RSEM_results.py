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
	result_text = sys.argv[3]

    #create dictionary from a single matrix data
	matrix_dict, sample_list = Matrix_Process_FL.READ_RSEM_MATRIX_DATA(matrix_dat)
	#KEY = SOMEKIND OF ID

#	print len(sample_list)
#	print len(set(list(sample_list)))
#	print matrix_dict['uc009fym.1','SRR805452']



	converter_info_dict = Matrix_Process_FL.READ_MATRIX_REFFLAT(converter_info)

	gene_symbol_list = []
	new_matrix_dict = {}

	#change dict key names
	for key in matrix_dict.keys():
		gene_id = key
		
		transcript_id = matrix_dict[key][0]
		length = matrix_dict[key][1]
		e_length = matrix_dict[key][2]
		e_count = matrix_dict[key][3]
		tpm = matrix_dict[key][4]
		fpkm = matrix_dict[key][5]

		gene_symbol = converter_info_dict[transcript_id]#NEW KEY
		gene_symbol_list.append(gene_symbol)

		new_info = [gene_symbol, length, e_length, e_count, tpm, fpkm]
		
		new_matrix_dict[gene_id] = new_info
	
	print 'Number of gene symbols', len(gene_symbol_list)
	gene_symbol_set_list = set(list(gene_symbol_list))
	print 'Number of set gene symbols', len(gene_symbol_set_list)



    #make matrix & output file
	Matrix_Process_FL.RSEM_MATRIX_TO_TEXT(new_matrix_dict, result_text, sample_list, gene_symbol_set_list)
	

#DONE
