"""
    This script makes a gene enrichment analysis using the Fisher´s exact test.
"""

import pandas as pd
import xlsxwriter
from scipy.stats import fisher_exact
import re

    
def counter (input_file):
    """Counts the lines which has a KEGG annotation."""
    count = 0
    for line in input_file:
        if line.startswith("M") and len(line.split()) == 2:
            count += 1
        else:
            continue
    return count


def find_num(text):
    """Searching for a number in lines in mapped file."""
    point = 0
    while text[text.find("(", point)+1:text.find(")", point)].isdigit() != True:
        point += 1
    return (str(text[text.find("(", point)+1:text.find(")", point)]))


def preprocessing_up_down_mapped_file(input_file):
    """Preprocessing the file with up/downregulated genes."""
    codes = []
    counts = []
    for line in input_file:        
        if line.find("(") != -1:
            num = find_num(line)
            codes.append(line[:5])
            counts.append(num)
    return(codes, counts)


def preprocessing_all_diff_mapped_file(input_file):
    """Preprocessing the file with mapped all differential expressed genes."""
    line_before = ""
    categories = {}
    subcategories = {}
    counts = []
    codes = []
    names = []
    count_sub = 0
    count_types = 0
    last_category = ""
    last_subcategory = ""
    for line in input_file:
        if line.find("(") != -1:
            if line_before != "": # line before is subcategory
                subcategories[last_subcategory[:-1]] = count_types
                last_subcategory = line_before
                #print("Last subcat" + str(last_subcategory))
                count_types = 0
                count_sub += 1
                line_before = ""       
            num = find_num(line)
            counts.append(num)
            codes.append(line[:5])
            names.append(line[5:line.find("("+str(num)+")")-1])
            count_types += 1
        else:
            if line_before == "":
                line_before = line
            else: # line before is category and this line is subcategory
                categories[last_category[:-1]] = count_sub
                subcategories[last_subcategory[:-1]] = count_types
                last_category = line_before
                last_subcategory = line
                count_sub = 1
                count_types = 0
                line_before = ""
    categories[last_category[:-1]] = count_sub
    subcategories[last_subcategory[:-1]] = count_types
    del categories['']
    del subcategories['']
    return (categories, subcategories, counts, codes, names)


def fisher_test(num_all, num_up_or_down, value_in_all, value_in_up_or_down):
    """Compute the fisher exact test."""
    not_in_up_or_down = value_in_all - value_in_up_or_down
    others_up_or_down = num_up_or_down - value_in_up_or_down
    others_not_in_up_or_down = num_all - others_up_or_down - not_in_up_or_down
    oddsratio, pvalue = fisher_exact([[value_in_up_or_down, not_in_up_or_down], [others_up_or_down, others_not_in_up_or_down]], alternative='greater')
    return(pvalue)


def write_line(line, row, header, worksheet):
    """Write the concerete line to the output file."""
    column = 0
    for word in line: 
        if header == 1:            
            worksheet.write(row, column, word, header_format)
            column += 1
        else:
            if column == 7 or column == 9:
                if float(word) <= signification:
                    worksheet.write(row, column, word, highlight_format)
                else:
                    worksheet.write(row, column, word)
            else:
                worksheet.write(row, column, word)
            column += 1
            

def writer (worksheet, num, row, category, subcategory, num_subcategory, values, down_values, up_values, names, codes, num_all, num_up, num_down):
    """Write the final excel file."""
    first_line = [num, category, subcategory, "{:.1f}".format(num_subcategory), subcategory, sum(values), sum(down_values), fisher_test(num_all, num_down, sum(values), sum(down_values)),\
            sum(up_values), fisher_test(num_all, num_up, sum(values), sum(up_values))]
    write_line(first_line, row, 1, worksheet)
    num += 1
    row += 1
    for i in range (0, len(values)):
        other_line=[num, category, subcategory, codes[i], names[i], values[i], down_values[i], fisher_test(num_all, num_down, int(values[i]), int(down_values[i])),\
             up_values[i], fisher_test(num_all, num_up, int(values[i]), int(up_values[i]))]
        write_line(other_line, row, 0, worksheet)
        num += 1
        row += 1
    return (num, row)


# Loading files
all_diff_expr_genes = open("IV_B_diff_exp_sign.txt", 'r')  # CHANGE THIS
upregulated_genes = open("IV_B_upregulated.txt", 'r')  # CHANGE THIS
downregulated_genes = open("IV_B_downregulated.txt", 'r')  # CHANGE THIS

all_mapped = open("IV_B_diff_exp_sign_mapped.txt", 'r')  # CHANGE THIS
up_mapped = open("IV_B_upregulated_mapped.txt", 'r')  # CHANGE THIS
down_mapped = open("IV_B_downregulated_mapped.txt", 'r')  # CHANGE THIS

# Preparing an output file
final_file = xlsxwriter.Workbook("B&IV_gene_enrichment.xlsx")  # CHANGE THIS
worksheet = final_file.add_worksheet()  # CHANGE THIS

header_line = ["B_down", "B_down", "B_up", "B_up"]  # CHANGE THIS
first_line = ["num", "pathway", "pathway", "pathway", "pathway", "ALL_(IV_B)", "log2F>2", "fisher_p-value_adj.",
              "log2F<-2", "fisher_p-value_adj."]
signification = 0.05

header_format = final_file.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'border': 1})
highlight_format = final_file.add_format({'bold': True, 'bg_color': 'yellow'})

column = 6
for word in header_line:
    worksheet.write(0, column, word, header_format)
    column += 1

column = 0
for word in first_line:
    worksheet.write(1, column, word, header_format)
    column += 1

# Processing the input mapped files
all_categories, all_subcategories, all_counts, all_codes, all_names = preprocessing_all_diff_mapped_file(
    all_mapped)
up_codes, up_counts = preprocessing_up_down_mapped_file(up_mapped)
down_codes, down_counts = preprocessing_up_down_mapped_file(down_mapped)

# Counts DE genes with KEGG annotation in input files
num_all = counter(all_diff_expr_genes)
num_up = counter(upregulated_genes)
num_down = counter(downregulated_genes)

# Setting the global variables
row = 2
num = 1
pointer = 0
point = 0
num_subcategory = 0.0

# Computing part of script with Fisher exact test
for category in all_categories.keys():
    num_subcategories = all_categories[category]
    num_subcategory += 0.9
    for i in range(point, point + num_subcategories):
        num_subcategory += 0.1
        up_values = []
        down_values = []
        names = []
        codes = []
        values = []
        subcategory = list(all_subcategories.keys())[i]
        num_types = list(all_subcategories.values())[i]
        for j in range(pointer, pointer + num_types):
            names.append(all_names[j])
            codes.append(int(all_codes[j]))
            values.append(int(all_counts[j]))
            if all_codes[j] in up_codes:
                up_values.append(int(up_counts[up_codes.index(all_codes[j])]))
            else:
                up_values.append(0)
            if all_codes[j] in down_codes:
                down_values.append(int(down_counts[down_codes.index(all_codes[j])]))
            else:
                down_values.append(0)
        pointer = pointer + num_types
        num, row = writer(worksheet, num, row, category, subcategory, num_subcategory, values,
                                                  down_values, up_values, names, codes, num_all, num_up, num_down)
    point += num_subcategories

worksheet.set_column(
    1,
    4,
    30)
final_file.close()
