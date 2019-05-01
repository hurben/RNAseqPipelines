################################################################
#FUNTION LIBRARY     1.0.0								15.01.15
#Matrix_Process_FL.py
################################################################


def READ_MATRIX_DATA(matrix_file):

	open_file = file(matrix_file)
	matrix_readlines = open_file.readlines()

	dict = {}


	for i in range(len(matrix_readlines)):
		read = matrix_readlines[i]
		read = read.replace('\n','')

		if i == 0:
			list = read.split('\t')

		if i != 0:

			token = read.split('\t')
			gene = token[0]
			if ',' in gene:
				gene = gene.split(',')[0]

			total_samples = len(token)
			
			for j in range(1,total_samples):
#				print j
#				if gene == 'uc009fym.1':
#					if list[j] == 'SRR805452':
#				if list[j] == 'SRR1041764':
#						print gene, list[j], token[j]
				dict[gene,list[j]] = token[j]

	return dict, list
		
	
def READ_RSEM_MATRIX_DATA(matrix_file):

	open_file = file(matrix_file)
	matrix_readlines = open_file.readlines()

	dict = {}


	for i in range(len(matrix_readlines)):
		read = matrix_readlines[i]
		read = read.replace('\n','')

		contents = []

		if i == 0:
			list = read.split('\t')

		if i != 0:

			token = read.split('\t')
			gene = token[0]
			transcript = token[1]
			if ',' in transcript:
				transcript = transcript.split(',')[0]


#			contents.append(gene)
			contents.append(transcript)

			
			for j in range(2, len(token)):
				contents.append(token[j])

			dict[gene] = contents




	return dict, list



	
def READ_MATRIX_REFFLAT(refflat_file):	
#WELL, technically it is not refflat. Though, I don't know the correct name.
#FILE NAME : mm10_kgXref
#source : UCSC
#0st column = KgID
#4th column = Gene symbol (Mouse symbol)
#ex) Tp53
#note that mouse symbol has capital only at the first character

	open_file = file(refflat_file)
	refflat_readlines = open_file.readlines()

	dict = {}

	for i in range(len(refflat_readlines)):
		read = refflat_readlines[i]
		read = read.replace('\n','')
		
		token = read.split('\t')
		kgID = token[0]
		gene = token[4]
		dict[kgID] = gene
			

	return dict



def MATRIX_TO_TEXT(dict,text,sample_list,gene_symbol_list):

	sample_list.pop(0) #exclude named "GENE" from list
	
	result_text = file(text,'w')

	result_text.write('gene')
	for sample_id in sample_list:
		result_text.write('\t'+str(sample_id))
	result_text.write('\n')

	


	for gene in gene_symbol_list:

		result_text.write(str(gene))
		for sample_id in sample_list:
			fpkm = dict[gene,sample_id]
			result_text.write('\t' + str(fpkm))
		result_text.write('\n')



def RSEM_MATRIX_TO_TEXT(dict,text,sample_list,gene_symbol_list):


	
	result_text = file(text,'w')

	result_text.write('gene_id\ttranscript_id(s)\tlength\teffective_length\texpected_count\tTPM\tFPKM\n')

	gene_id_list = []

	for i in dict.keys():
		i = int(i)
		gene_id_list.append(i)


	sorted_gene_id_list = sorted(gene_id_list)

#	for gene_id in dict.keys():
	for gene_id in sorted_gene_id_list:

		result_text.write(str(gene_id))
		
		gene_id = str(gene_id)

		gene = dict[gene_id][0]


		result_text.write('\t' + str(gene) + '\t' + str(dict[gene_id][1]) + '\t' + str(dict[gene_id][2]) + '\t' + str(dict[gene_id][3]) + '\t' + str(dict[gene_id][4]) + '\t' + str(dict[gene_id][5]) +'\n')





