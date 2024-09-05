from Bio import SeqIO
from Bio.Seq import Seq
#from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord
import os
import argparse


# Set up an arg parse to get user arguments
parser = argparse.ArgumentParser(description='script for running fasta cleaning')

#Add arguments
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Full path to a CDS fasta file to be cleaned') 
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Full path to a new AA fasta file to be output (file should not exist before running)') 

#Define the parser
args = parser.parse_args()

input_fasta=args.input
output_fasta=args.output

# Function to translate DNA sequences to protein sequences
def translate_cds_to_protein(cds_sequence):
    return cds_sequence.translate(to_stop=True)

# Read the input FASTA, translate sequences, and write to output FASTA
with open(output_fasta, "w") as output_handle:
    for record in SeqIO.parse(input_fasta, "fasta"):
        #print(str(record.seq)[0:3])
        #print(len(str(record.seq)) % 3)
        
        if str(record.seq)[0:3] == "ATG" and len(str(record.seq)) % 3 == 0:
            # Translate the CDS sequence
            protein_seq = translate_cds_to_protein(record.seq)
            
            # Create a new SeqRecord for the translated protein sequence
            protein_record = SeqRecord(protein_seq, id=record.id, description="")
            
            # Write the translated sequence to the output file
            SeqIO.write(protein_record, output_handle, "fasta")
        else:
            print(f"Dropping {record.id} because it didn't start with ATG or wasn't a multiple of 3")

print(f"Protein sequences have been written to {output_fasta}.")


