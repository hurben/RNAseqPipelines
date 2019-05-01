##################################################################
#NONCAFFGENE_DEG_selection_by_foldchange.py			   15.04.09
#
#
#Description : [1] Read matrix from resulted file. 
#				ex) Gata3_symbol.matrix
#
#			   [2] define which column to use as WT & KO
#				ex) because we cannot handle biological replicates at once
#
#	           [3] input which foldchange to use. by default 1.6
#
#################################################################
#Important note
#Matrix file format : column = samples, row[0] = sample name, row[n+1] = FPKM



def files_to_dict(matrix_file, wt_column, ko_column, fpkm_dict):
	
	matrix_open = file(matrix_file)
	matrix_readlines = matrix_open.readlines()

	for i in range(1, len(matrix_readlines)):
		read = matrix_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')
		gene = token[0]
		wt_fpkm = token[wt_column]
		ko_fpkm = token[ko_column]

		if gene in fpkm_dict:
			print "Duplicated gene exist! Check matrix file!! : " , gene
		else:
			fpkm_dict[gene] = [wt_fpkm, ko_fpkm]
		
		
	
def calculate_fc(fpkm_dict,fc, result_dict):
	
	for gene in fpkm_dict.keys():
		wt = float(fpkm_dict[gene][0])
		ko = float(fpkm_dict[gene][1])


		if wt != 0 and ko != 0:
			current_fc_1 = ko / wt
			current_fc_2 = wt / ko

			status = 'none'
			if current_fc_1 >= fc or current_fc_2 >= fc:

				if current_fc_1 >= fc:
					status = 'upregulated'
					value = current_fc_1

				if current_fc_2 >= fc:
					status = 'downregulated'
					value = current_fc_2

				result_dict[gene] = [value,status]
				

def result_to_text(result_dict, txt):	

	for genes in result_dict.keys():
		value = result_dict[genes][0]
		status = result_dict[genes][1]

		txt.write(str(genes) +'\t' + str(value) + '\t' + str(status) +'\n')
			
		



#starting Program : NONCAFFGENE_DEG_selection_by_foldchange.py

if __name__ == '__main__':


	import sys
	import argparse
	import subprocess
	import os

	#location of bin folder : in other words, the program location
	program_dir = os.path.split(os.path.realpath(__file__))

	#call library path & function : error_check
	lib_path = os.path.abspath(str(program_dir[0])+'/')

	#Using Argparse for Option retrival
	parser = argparse.ArgumentParser()	#initialize argparse

	#Note : n = row, m = column
	parser.add_argument('-i','--input', dest = 'input_file', help="Assign input file")
	parser.add_argument('-wt','--wild_type', dest = 'WT_column', help="Where is WT column?")
	parser.add_argument('-ko','--knock_out', dest = 'KO_column', help = "Where is KO column" ) 
	parser.add_argument('-fc','--fold_change', dest = 'defined_fc', help = "Which fold change to use?" ) 
	parser.add_argument('-o','--output', dest = 'output', help = "output text file name" ) 
	args= parser.parse_args()


	#Defining argument variables
	matrix_file = args.input_file
	wt_column = args.WT_column
	ko_column = args.KO_column
	fc = args.defined_fc
	output_txt = args.output

	fpkm_dict = {}
	fc_fpkm_dict = {}
	result_dict = {}

	if fc == None:
		print "[Notice] FC rate not given. Using default foldchange rate."
		fc = '1.6'
	fc = float(fc)
	wt_column = int(wt_column)
	ko_column = int(ko_column)

	if output_txt == None:
		result_text = file(str(matrix_file) + 'fc.deg','w')
	if output_txt != None:
		result_text = file(str(output_txt),'w')


	#Main program
	
	files_to_dict(matrix_file, wt_column, ko_column, fpkm_dict)
	calculate_fc(fpkm_dict,fc, result_dict)
	result_to_text(result_dict, result_text)


