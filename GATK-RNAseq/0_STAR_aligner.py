#----------------------------------------------------
#1_STAR_aligner.py						15.04.13
#
#
#
#
#
#
#
#
#
#-----------------------------------------------------

#CAUTION
#FOR NON-PAIR END DATA
#LIST INPUT
#path/file_1.fastq[tab]path/file_2.fastq




import os
import sys

genome_dir = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF/'
genome_file = '//data/project/CAFFGENE_EXTENDED/data/ref_data/STAR_REF/mmu10_refseq.fa'
gtf_file = '//data/project/CAFFGENE_EXTENDED/data/ref_data/mmu10.gtf'
star_file ='//data/project/CAFFGENE_EXTENDED/packages/STAR-STAR_2.4.0k/source/STAR'

size = '49'


#cmd = str(star_file) +' --runThreadN 8 --runMode genomeGenerate --genomeDir ' + str(genome_dir) + ' --genomeFastaFiles ' +str(genome_file) + ' --sjdbGTFfile ' + str(gtf_file) + ' --sjdbOverhang ' + str(size)
cmd = str(star_file) +' --runThreadN 8 --runMode genomeGenerate --genomeDir ' + str(genome_dir) + ' --genomeFastaFiles ' +str(genome_file)
print cmd

os.system(cmd)


