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
    if last_transcript == transcript and concrete_gene == 1: # transkript s jiz zapsanym genem - ignoruju
        continue
    elif last_transcript == transcript and concrete_gene == 0: # dalsi z nabizenych genu pro dany transkript
        gene = splitter[2]
        if any(un in gene for un in unknown):
            concrete_gene = 0
        else:
            concrete_gene = 1
            output_file.write(line)
    else: # muzu zacit prozkoumavat novy transkript
        if last_transcript != transcript and concrete_gene == 0 and last_transcript != "": # transcript, ktery ma vsechny geny unknown, tak je treba zapsat ten prvni ulozeny
            output_file.write(first_line)
        last_transcript = transcript
        first_line = line # ulozeno pro pripad, ze by vsechny vyskyty obsahovaly unknown
        gene = splitter[2]
        if any(un in gene for un in unknown):
            concrete_gene = 0
        else:
            concrete_gene = 1
            output_file.write(line)
