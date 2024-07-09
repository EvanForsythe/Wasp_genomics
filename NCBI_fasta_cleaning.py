# load the needed modules
from Bio import SeqIO
import re
import sys
import os
import argparse

#Example command:
#python NCBI_fasta_cleaning.py -i /scratch/forsythe/ERC_collaborations/Parasitoid_wasp_data/Data_downloads/Leptopilina_boulard/ncbi_dataset/data/GCF_019393585.1/cds_from_genomic.fna -o /scratch/forsythe/ERC_collaborations/Parasitoid_wasp_data/Wasp_genomics/example_data/Leptopilina_boulard_prot_CLEANED.fa

# Set up an arg parse to get user arguments
parser = argparse.ArgumentParser(description='script for running fasta cleaning')

#Add arguments
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Full path to a CDS fasta file to be cleaned') 
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Full path to a new fasta file to be output (file should not exist before running)') 

#Define the parser
args = parser.parse_args()

input=args.input
output=args.output


#Check to make sure input file exists
if os.path.isfile(input):
    print("Found input file!")
else:
    print("ERROR: Couldn't find input file. Check that your -i argument is correct")
    sys.exit()

#Check to make sure output file doesn't exist
if os.path.isfile(output):
    print("ERROR: output file already exists. Delete or rename existing file before running.")
    sys.exit()
else:
    print(f"Output will be stored in: {output}")

# Read the file in to python and store as a dictionary object
input_file = open(input)
my_dict = SeqIO.to_dict(SeqIO.parse(input_file, "fasta"))

#temp_record=my_dict['lcl|NW_026138046.1_cds_XP_051175781.1_23824']

#print(temp_record.description)


# Loop through each of the dictionary items and do the following for each:
    # Ask if the id contains "Isoform"
        #If so, ask if ID contains "X1"
    # Extract only the fields of interst

#make a blank list
check_list=[]

file_handle=open(output, "a")

for key in my_dict:
    #Subset the dictionary
    temp_record=my_dict[key]

    #Get the description and seq
    temp_desc=temp_record.description
    temp_seq=temp_record.seq

    # Regular expression to match the protein field
    prot_pattern = r'\[protein=(.*?)\]'

    # Search for the pattern in the line
    prot_match = re.search(prot_pattern, temp_desc)

    # If a match is found, extract the protein name
    if prot_match:
        prot_desc = prot_match.group(1)
    else:
        prot_desc = "NA"

    # Regular expression to match prot_id
    id_pattern = r'\[protein_id=(.*?)\]'

    # Search for the pattern in the line
    id_match = re.search(id_pattern, temp_desc)

    # If a match is found, extract the protein name
    if id_match:
        prot_id = id_match.group(1)
    else:
        prot_id = "NA"


    #NOTE: Still need to figure out how to remove isoform X11
    if not prot_desc in check_list:
        #print(f"found duplicate: {id_desc} {prot_desc}")
        if "isoform X" in prot_desc:
            keeper_bool=False
            if "isoform X1" in prot_desc and not "isoform X11" in prot_desc:
                #print(prot_desc)
                keeper_bool=True
            else:
                keeper_bool=False
        else: 
            #print(prot_desc)
            keeper_bool=True
    else:
        keeper_bool=False
    
    if keeper_bool:
        file_handle.write(">"+prot_id+"__"+prot_desc+"\n")
        file_handle.write(str(temp_seq)+"\n")

    check_list.append(prot_desc)

file_handle.close()
    


    




