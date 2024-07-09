# load the needed modules
from Bio import SeqIO
import re
import sys

# get the full path to the file I want to clean
file_path = "/scratch/forsythe/ERC_collaborations/Parasitoid_wasp_data/Leptopilina_boulard/ncbi_dataset/data/GCF_019393585.1/cds_from_genomic.fna"

# Read the file in to python and store as a dictionary object
input_file = open(file_path)
my_dict = SeqIO.to_dict(SeqIO.parse(input_file, "fasta"))

#temp_record=my_dict['lcl|NW_026138046.1_cds_XP_051175781.1_23824']

#print(temp_record.description)


# Loop through each of the dictionary items and do the following for each:
    # Ask if the id contains "Isoform"
        #If so, ask if ID contains "X1"
    # Extract only the fields of interst

#make a blank list
check_list=[]

file_handle=open("keeper_file.fasta", "a")

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


    


    




