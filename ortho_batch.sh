#!/bin/bash
#SBATCH --job-name=ortho
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=96
#SBATCH --time=96:0:0
#SBATCH --output=ortho.out
#SBATCH --error=ortho.err
#SBATCH --mail-user=evan.forsythe@osucascades.edu
#SBATCH --mail-type=END

# Load a module, if needed
#module load python/anaconda/3.11
#source activate orthofinder-env

# Change to the working directory
# cd /home/other/forsythe/ERC_project/BirdERC/

echo "starting orthofinder"
echo `date "+%Y-%m-%d %H:%M:%S"`

# Commands
orthofinder -f /scratch/forsythe/ERC_collaborations/Parasitoid_wasp_data/Wasp_genomics/input_file_versions/translated_prots/ -y -X -M msa -t 96 -o /scratch/forsythe/ERC_collaborations/Parasitoid_wasp_data/Wasp_genomics/Orthofinder_output/

echo "finishing orthofinder"
echo `date "+%Y-%m-%d %H:%M:%S"`


#orthofinder -f /home/forsythe/Projects/ERC/BirdERC/Bird_fastas/ -s /home/forsythe/Projects/ERC/BirdERC/Bird_tree_1line.newick -y -X -M msa -t 96 -o /scratch/forsythe/Orthofinder_output/
