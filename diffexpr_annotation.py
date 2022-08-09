""" 
    This script merge the table of differential expressed transcripts of individual pairs of replicates (B&IV, ICR&IV, B&ICR) with KEGG and NCBI
    annotations based on the unique identifier of each transcript
"""

import pandas as pd
import re
import numpy as np

# Make output Pandas Excel writer using XlsxWriter as the engine
output_name = "B&ICR_diffexprese_anotace.xlsx" # CHANGE THIS
writer = pd.ExcelWriter(output_name, engine = 'xlsxwriter')

# Reading the first file = output of DeSeQ2
diffexpr = pd.read_csv("diffexpr-results_b_icr.csv",delimiter=',',header=0) # CHANGE THIS
new_columns = diffexpr.columns.values
new_columns[0] = 'Numbers'
diffexpr.columns = new_columns
diffexpr.set_index("Numbers",drop=True,inplace=True)

# Reading the ncbi file
ncbi = pd.read_csv("BLASTP_M_corti.PRJEB510.WBPS15.protein_NCBI_final.txt",delimiter='\t',header=None) # CHANGE THIS
ncbi.rename(columns={0: 'Gene', 1: 'sseqid', 2: 'NCBI_anno', 3: 'pident', 4: 'length', 5: 'mismatch', 6: 'gapopen', 7: 'qstart', 8: 'qend',
                     9: 'sstart', 10: 'send', 11: 'evalue', 12: 'bitscore' }, inplace = True)

# Reading the KEGG file
KEGG = pd.read_csv("KEGG_anno_ghost_koala_ref_proteome_PRJEB510.WBPS15.txt",delimiter='\t',header=None) # CHANGE THIS
KEGG.rename(columns = {0: 'Gene', 1:'KEGG_ID', 2:'KEGG_anno'}, inplace = True)

# Outher joining of files by specific column ('Gene')
outer_file = pd.merge(diffexpr, ncbi, how="outer", on=["Gene"])
outer_file2 = pd.merge(outer_file, KEGG, how="outer", on = ["Gene"])

# Get the right order of columns
all_data = outer_file2[['Gene','KEGG_ID','KEGG_anno','NCBI_anno','baseMean','log2FoldChange','lfcSE','stat','pvalue','padj',
                        'B1','B2','B3','B4','ICR1','ICR2','ICR3','ICR4']]
all_data.to_excel(writer, sheet_name='all_data')

# Have only the columns with padj. < 0.05
right_data = all_data.loc[all_data['padj'] <= 0.05]
right_data.to_excel(writer, sheet_name='data_padj<0.05')

# Filtering the data by lof2FoldChange
## high_upregulated
high_upregulated = right_data.loc[right_data['log2FoldChange'] > 2]
high_upregulated.to_excel(writer, sheet_name='log2FoldChange>2')

## upregulated
upregulated = right_data.loc[(right_data['log2FoldChange'] > 1) & (right_data['log2FoldChange'] <= 2)]
upregulated.to_excel(writer, sheet_name='log2FoldChange1-2')

## slightly_upregulated
slightly_upregulated = right_data.loc[(right_data['log2FoldChange'] > 0) & (right_data['log2FoldChange'] <= 1)]
slightly_upregulated.to_excel(writer, sheet_name='log2FoldChange0-1')

## slightly_downregulated
slightly_downregulated = right_data.loc[(right_data['log2FoldChange'] > -1) & (right_data['log2FoldChange'] <= 0)]
slightly_downregulated.to_excel(writer, sheet_name='log2FoldChange-1-0')

## downregulated
downregulated = right_data.loc[(right_data['log2FoldChange'] > -2) & (right_data['log2FoldChange'] <= -1)]
downregulated.to_excel(writer, sheet_name='log2FoldChange-2-(-1)')

## high_downregulated
high_downregulated = right_data.loc[right_data['log2FoldChange'] <= -2]
high_downregulated.to_excel(writer, sheet_name='log2FoldChange<-2')

writer.save()
