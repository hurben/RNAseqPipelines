def make_dir(folder_name):
	make_dir = 'mkdir ' +str(folder_name)
	os.system(make_dir)
		

def build_initial_genome(star_package, ref_seq_dir, ref_seq):
	cmd = str(star_package) +' --runThreadN 8 --runMode genomeGenerate --genomeDir ' + str(ref_seq_dir) + ' --genomeFastaFiles ' +str(ref_seq)
	os.system(cmd)


def first_pass_genome_alignment(star_package, ref_seq_dir, file_with_dir, prefix_dir):
	cmd = str(star_package) +' --runThreadN 8 --genomeDir ' + str(ref_seq_dir) + ' --readFilesIn ' +str(file_with_dir) + ' --outFileNamePrefix ' +str(prefix_dir)
	print "[NOTE] Executing 1st pass Genome alignment : " , cmd
	os.system(cmd)


def	second_pass_genome_generate(star_package, second_prefix_dir, ref_seq, prefix_dir, size, sj_out_file):
	#generate genome
	cmd = str(star_package) +' --runThreadN 8 --runMode genomeGenerate --genomeDir ' +str(second_prefix_dir) + ' --genomeFastaFiles ' +str(ref_seq) +' --sjdbFileChrStartEnd ' + str(prefix_dir) + '/' + str(sj_out_file) + ' --sjdbOverhang ' + str(size) +' --outFileNamePrefix ' +str(second_prefix_dir)
	print "[NOTE] Executing 2nd pass Genome Generation : " , cmd
	os.system(cmd)

def second_pass_genome_alignment(star_package, second_prefix_dir, file_with_dir):
	cmd = str(star_package) +' --runThreadN 8 --genomeDir ' + str(second_prefix_dir) + ' --readFilesIn ' +str(file_with_dir) + ' --outFileNamePrefix ' +str(second_prefix_dir)
	print "[NOTE] Executing 2nd pass Genome alignment : " , cmd
	os.system(cmd)


def add_groups(picard_dir, second_prefix_dir, master_dir, add_readgroup_out):

	cmd = 'java -jar ' + str(picard_dir)+'AddOrReplaceReadGroups.jar I=' +str(second_prefix_dir) + '/Aligned.out.sam O='+str(Master_dir) + '/' +str(add_readgroup_out)+ ' SO=coordinate RGID=id RGLB=library RGPL=platform RGPU=machine RGSM=sample'
	print "[NOTE] Executing Add or Replace ReadGroups : " , cmd
	os.system(cmd)


def mark_duplicates(picard_dir, result_of_add_readgroup, result_of_markdup):
	cmd = 'java -jar ' + str(picard_dir)+ 'MarkDuplicates.jar I=' +str(result_of_add_readgroup)+ ' O=' + str(result_of_markdup)+ ' CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M='+str(result_of_markdup)+'.metrics'
	print "[NOTE] Executing MarkDuplicates : " , cmd
	os.system(cmd)


def splitNtrim(gatk_package, ref_seq, input_splitNtrim, output_splitNtrim):
	cmd = 'java -jar ' + str(gatk_package) +' -T SplitNCigarReads -R ' +str(ref_seq) + ' -I ' +str(input_splitNtrim) + ' -o ' +str(output_splitNtrim) + ' -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS --fix_misencoded_quality_scores -fixMisencodedQuals'
	print "[NOTE] Executing SplitNCigarReads : " , cmd
	os.system(cmd)


def haplotypecaller(gatk_package, ref_seq, input_variant_calling, output_variant_calling):
	cmd = 'java -jar ' + str(gatk_package) +' -T HaplotypeCaller -R ' +str(ref_seq) + ' -I ' +str(input_variant_calling) + ' -o ' +str(output_variant_calling) + ' -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS --fix_misencoded_quality_scores -fixMisencodedQuals'
	print "[NOTE] Executing HaplotypeCaller : " , cmd
	os.system(cmd)



#Mutation calling , GATK-RNA-seq 

#All in one


if __name__ == '__main__':


	import sys
	import argparse
	import subprocess
	import os

	#declare package
	star_package = '//data/project/CAFFGENE_EXTENDED/packages/STAR-STAR_2.4.0k/source/STAR'
	picard_dir = '//data/project/CAFFGENE_EXTENDED/packages/picard/picard-tools-1.115/'
	gatk_package = '//data/project/CAFFGENE_EXTENDED/packages/GenomeAnalysisTK.jar'


	#location of bin folder : in other words, the program location
	program_dir = os.path.split(os.path.realpath(__file__))

	#call library path & function : error_check
	lib_path = os.path.abspath(str(program_dir[0])+'/')

	#Using Argparse for Option retrival
	parser = argparse.ArgumentParser()	#initialize argparse

	#Note : n = row, m = column
	parser.add_argument('-rd','--ref_dir', dest = 'ref_seq_dir', help="")
	parser.add_argument('-rf','--ref_file', dest = 'ref_seq', help="")
	parser.add_argument('-r','--readlength', dest = 'readlength', help = "" ) 
	parser.add_argument('-fl','--fasta_list', dest = 'fq_list', help = "" ) 
	parser.add_argument('-f','--initial_genome_build', dest = 'flag', help = "" ) 
	#IMPORTANT!!
	#DO -s if you did not made an intial genome build for your REF_SEQ
	#HOWEVER , WHEN THIS PROCESS IS DONE. YOU DO NOT NEED THIS PROCESS.
	#Which means for if you are reusing intial_genome_build. do not input -s

	args= parser.parse_args()


	#Defining argument variables
	ref_seq_dir = args.ref_seq_dir
	ref_seq = args.ref_seq
	size = args.readlength

	fq_list = args.fq_list
	fq_list_file = file(fq_list)
	fq_list_readlines = fq_list_file.readlines()


	flag = args.flag

#STEP 1 : STAR

#Needs
#[1] Ref fasta file dir
#[2] dir/fasta file 


#1-1 Initial genome build ( pre- 1pass)
	if flag != None:
		print "Doing genome build"
		#RUN INTIAL GENOME BUILD
		build_initial_genome(star_package, ref_seq_dir,ref_seq)
	
#1-2 pass1	


	#read from file
	for i in range(len(fq_list_readlines)):
		read = fq_list_readlines[i]
		read = read.replace('\n','')

		file_with_dir = read
		token = read.split('/')
		file_name = token[len(token) -1]
		out_name = str(file_name)+'.1st_pass'



		#making sample_tagged dir ex) gata3
		make_dir(file_name)



########Making Master folder
		Master_dir = './' + str(file_name)

		print "[[[[[[[[[[[[[[ NOTE ]]]]]]]]]]]]]]"
		print "         " + str(file_name) 
		print "[[[[[[[[[[[[[[ NOTE ]]]]]]]]]]]]]]"

		print "--- STAR 1st pass ---"
		make_1pass_dir = str(Master_dir) + '/1st_pass'
		make_dir(make_1pass_dir)

		print "[NOTE] Making 1st pass directory : " , make_1pass_dir

		#Master folder
		#    -1st pass folder

########1st folder buffer
		pass1_folder = '/1st_pass/'
		prefix_dir = str(Master_dir) + str(pass1_folder)


		print "[NOTE] 1st Pass results stores at : " , prefix_dir

		#RUN : genome align
		first_pass_genome_alignment(star_package, ref_seq_dir, file_with_dir, prefix_dir)


#########file buffer : FIXED VARIABLE
		sj_out_file = 'SJ.out.tab'

#1-3 pass2
		print "--- STAR 2nd pass ---"


########2nd folder buffer
		make_2pass_dir = str(Master_dir)+ '/2nd_pass'
		make_dir(make_2pass_dir)

		#Master folder
		#   -2nd pass folder
		print "[NOTE] Making 2nd pass directory : " , make_2pass_dir


		second_prefix_dir = str(Master_dir) + '/2nd_pass/'
		print "[NOTE] 2nd Pass results stores at : " , second_prefix_dir


		#RUN : generate genome
		second_pass_genome_generate(star_package, second_prefix_dir, ref_seq, prefix_dir, size, sj_out_file)
		
		#RUN : genome align
		second_pass_genome_alignment(star_package, second_prefix_dir, file_with_dir)



#STEP 2 : Picard

		print " --- Picard process --- "

		add_readgroup_out = str(file_name) + ".added_sorted.bam"


		#RUN add or replace groups
		add_groups(picard_dir, second_prefix_dir,Master_dir,add_readgroup_out)
		

########FOLDER , OUTPUT BUFFER
		result_of_add_readgroup = str(Master_dir) + '/' + str(add_readgroup_out)
		result_of_markdup = str(result_of_add_readgroup) + '.dedupped.bam'

				
		#RUN markduplicates
		mark_duplicates(picard_dir, result_of_add_readgroup, result_of_markdup)


#STEP 3 : SplitNTrim
		print " --- SplitNTrim --- "

########FOLDER , OUTPUT BUFFER
		input_splitNtrim = result_of_markdup #dedupped.bam file
		output_splitNtrim = str(Master_dir) + '/' + str(file_name) +'.split.bam'


		#RUN splitNtrim
		splitNtrim(gatk_package, ref_seq, input_splitNtrim, output_splitNtrim)
	


#STEP 4 : Variant calling
		print " --- Variant Calling --- "

		mkdir_vcf_result_folder = str(Master_dir) + '/VCF'
		make_dir(mkdir_vcf_result_folder)

		input_variant_calling = output_splitNtrim
		output_variant_calling = str(Master_dir) + '/VCF/' + str(file_name) + '.vcf'

		haplotypecaller(gatk_package, ref_seq, input_variant_calling, output_variant_calling)
		
	


