


def read_from_list_of_files(list_of_files):

	list_of_files_readlines = list_of_files.readlines()

	for i in range(len(list_of_files_readlines)):
		read = list_of_files_readlines[i]
		read = read.replace('\n','')

		token = read.split('\t')
		path = read
		file_name = token[len(token) -1]
		readlines_from_file


def readlines_from_file(file_with_path):

	input_file = file(file_with_path)
	input_file_readlines = input_file.readlines()
