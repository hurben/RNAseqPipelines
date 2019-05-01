####################################################
#FPKM_check.py                              14.12.11
#
#
#description : After using rsem's rsem-calculate-expression
#			   Checking as if the files are successfuly have FPKM.
#
#
#command line : python FPKM_check [list of files]
####################################################
#list of files 
#/path/"FILE_NAME".genes.results


import sys
import os

program_dir = os.path.split(os.path.realpath(__file__)) #location of bin folder
lib_path = os.path.abspath(str(program_dir[0])+'/')

import library

#argv
list_of_files_argv = sys.argv[1]
list_of_files = file(list_of_files_argv)


library.read_from_list_of_files(list_of_files)




	
