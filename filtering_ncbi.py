"""
   This script is used to select one specific annotation from 5 different NCBI annotations for each transcript primarily based
   on the gene's functional annotation and secondary based on the highest bit_score value.
"""


import re
input_file = open("BLASTP_M_corti.PRJEB510.WBPS15.protein_NCBI.txt", 'r')
output_file = open ("BLASTP_M_cort.PRJEB510.WBPS15.protein_NCBI_final_lucka.txt", 'a+')



gene = ""
concrete_gene = 0
last_transcript = ""
first_line = ""
unknown = ["unknown", "hypothetical", "unnamed"]
for line in input_file:
    splitter = re.split('\t', line)
    transcript = splitter[0]
    if last_transcript == transcript and concrete_gene == 1: # transcript with concrete annotation
        continue
    elif last_transcript == transcript and concrete_gene == 0: # transcript with no concrete annotation
        gene = splitter[2]
        if any(un in gene for un in unknown):
            concrete_gene = 0
        else:
            concrete_gene = 1
            output_file.write(line)
    else:
        if last_transcript != transcript and concrete_gene == 0 and last_transcript != "": # transcript with all unknown annotations, write the first annotation
            output_file.write(first_line)
        last_transcript = transcript
        first_line = line # the first annotation
        gene = splitter[2]
        if any(un in gene for un in unknown):
            concrete_gene = 0
        else:
            concrete_gene = 1
            output_file.write(line)
