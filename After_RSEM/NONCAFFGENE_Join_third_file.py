##################################################################
#NONCAFFGENE_Join_two_files.py						   15.04.13
#
#
#Description : [1] Read 2 matrix from resulted 2 file. 
#				ex) Gata3_1.6deg.sample1 Gata3_1.6deg.sample2
#
#
#################################################################


def files_to_dict_case1(matrix_file, matrix_dict):
	
	matrix_open = file(matrix_file)
	matrix_readlines = matrix_open.readlines()

	for i in range(len(matrix_readlines)):
		read = matrix_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')
		gene = token[0]
		fc = token[1]
		second_fc = token[2]
		status = token[3]

		if gene in matrix_dict:
			print "Duplicated gene exist! Check matrix file!! : " , gene
		else:
			matrix_dict[gene] = [fc, second_fc,status]


def files_to_dict_case2(matrix_file, matrix_dict):

	matrix_open = file(matrix_file)
	matrix_readlines = matrix_open.readlines()

	for i in range(len(matrix_readlines)):
		read = matrix_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')
		gene = token[0]
		fc = token[1]
		status = token[2]

		if gene in matrix_dict:
			print "Duplicated gene exist! Check matrix file!! : " , gene
		else:
			matrix_dict[gene] = [fc, status]

def intersection_among_files(matrix_1_dict, matrix_2_dict, result_dict):

	for gene in matrix_1_dict.keys():

		if gene in matrix_2_dict.keys():

			fpkm_1 = matrix_1_dict[gene][0]
			fpkm_2 = matrix_1_dict[gene][1]
			fpkm_3 = matrix_2_dict[gene][0]

			status_1 = matrix_1_dict[gene][2]
			status_2 = matrix_2_dict[gene][1]

			if status_1 == status_2:

				result_dict[gene] = [fpkm_1, fpkm_2 ,fpkm_3, status_1, status_1, status_2]


def result_to_text(result_dict, txt):	

	for genes in result_dict.keys():

		fpkm_1 = result_dict[genes][0]
		fpkm_2 = result_dict[genes][1]
		fpkm_3 = result_dict[genes][2]

		status_1 = result_dict[genes][3]
		status_2 = result_dict[genes][4]
		status_3 = result_dict[genes][5]

		txt.write(str(genes) + '\t' + str(fpkm_1) + '\t' + str(fpkm_2) + '\t' + str(fpkm_3) + '\t' + str(status_1) + '\t' + str(status_1) + '\t' +  str(status_2) + '\t' + str(status_3) +'\n')
	


#starting Program : NONCAFFGENE_Join_two_files.py

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
	parser.add_argument('-i1','--input_1', dest = 'input_1_file', help="Assign input file")
	parser.add_argument('-i2','--input_2', dest = 'input_2_file', help="Assign input file")
	parser.add_argument('-o','--output', dest = 'output', help = "output text file name" ) 
	args= parser.parse_args()


	#Defining argument variables
	matrix_1_file = args.input_1_file
	matrix_2_file = args.input_2_file
	output_txt = args.output
	output_txt =file(output_txt,'w')


	matrix_1_dict = {}
	matrix_2_dict = {}
	result_dict = {}


	#Main program
	
	files_to_dict_case1(matrix_1_file, matrix_1_dict)
	files_to_dict_case2(matrix_2_file, matrix_2_dict)

	intersection_among_files(matrix_1_dict, matrix_2_dict, result_dict)
	result_to_text(result_dict,output_txt)

