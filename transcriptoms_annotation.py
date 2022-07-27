import pandas as pd
import re
import numpy as np

# Make output Pandas Excel writer using XlsxWriter as the engine
output_name = "IV_annotation.xlsx" # CHANGE THIS
writer = pd.ExcelWriter(output_name, engine = 'xlsxwriter')

# Reading the input file from the RSEM
input_file = pd.read_csv("IV_file.csv", delimiter=';', header=0) # CHANGE THIS
input_file

# Reading the ncbi file
ncbi = pd.read_csv("BLASTP_M_corti.PRJEB510.WBPS15.protein_NCBI_final.txt",delimiter='\t',header=None) # CHANGE THIS
ncbi.rename(columns={0: 'TranscriptID', 1: 'sseqid', 2: 'NCBI_anno', 3: 'pident', 4: 'length', 5: 'mismatch', 6: 'gapopen', 7: 'qstart', 8: 'qend', 9: 'sstart', 10: 'send', 11: 'evalue', 12: 'bitscore' }, inplace = True)

# Reading the KEGG file
KEGG = pd.read_csv("KEGG_anno_ghost_koala_ref_proteome_PRJEB510.WBPS15.txt",delimiter='\t',header=None) # CHANGE THIS
KEGG.rename(columns = {0: 'TranscriptID', 1:'KEGG_ID', 2:'KEGG_anno'}, inplace = True)

# Outer joining of files by specific column ('Gene')
outer_file = pd.merge(input_file, ncbi, how="outer", on=["TranscriptID"])
outer_file2 = pd.merge(outer_file, KEGG, how="outer", on = ["TranscriptID"])

# Get the right order of columns
all_data = outer_file2[['TranscriptID','KEGG_ID','KEGG_anno','NCBI_anno','IV_expectedCount','IV2_expectedCount','IV3_expectedCount','IV4_expectedCount','IV_TPM','IV2_TPM','IV3_TPM','IV4_TPM']]
right_data = all_data.loc[(all_data['IV_expectedCount']>=10) & (all_data['IV2_expectedCount']>=10) & (all_data['IV3_expectedCount']>=10) & (all_data['IV4_expectedCount']>=10)]
right_data.to_excel(writer)

writer.save()
