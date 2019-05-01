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
	matrix_dict, sample_list = Matrix_Process_FL.READ_MATRIX_DATA(matrix_dat)
	#KEY = SOMEKIND OF ID

#	print len(sample_list)
#	print len(set(list(sample_list)))
#	print matrix_dict['uc009fym.1','SRR805452']



	converter_info_dict = Matrix_Process_FL.READ_MATRIX_REFFLAT(converter_info)

	gene_symbol_list = []

	#change dict key names
	for key in matrix_dict.keys():
		transcript_id = key[0]
		sample_id = key[1]
		gene_symbol = converter_info_dict[transcript_id]#NEW KEY
		gene_symbol_list.append(gene_symbol)
		
		matrix_dict[gene_symbol,sample_id] = matrix_dict[key]
		del matrix_dict[key]
	
	print 'Number of gene symbols', len(gene_symbol_list)
	gene_symbol_set_list = set(list(gene_symbol_list))
	print 'Number of set gene symbols', len(gene_symbol_set_list)

	


    #make matrix & output file
	Matrix_Process_FL.MATRIX_TO_TEXT(matrix_dict, result_text, sample_list, gene_symbol_set_list)
	

#DONE
