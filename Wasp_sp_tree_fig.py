#import needed modules
import os
import sys
import pandas as pd
from Bio import Phylo
import matplotlib.pyplot as plt
import pastml

#read in the csv file and store as a dataframe object
taxon_df = pd.read_csv('Wasp_character_states.csv')


ecto_counter = 0
endo_counter = 0
non_counter = 0

for ind in taxon_df.index:
    temp_tax = taxon_df["Species_name"][ind]
    temp_char_state = taxon_df["Character_state"][ind]

    if temp_char_state == "Ecto":
        ecto_counter += 1 
    elif temp_char_state == "Endo":
        endo_counter += 1
    elif  temp_char_state == "Non":
        non_counter += 1
    else:
        print(f"ERROR! Invalid character state for {temp_tax}. Quitting...")
        sys.exit()


if len(taxon_df.index) == ecto_counter+endo_counter+non_counter:
    print(f"Total number of species included is {len(taxon_df.index)}")
else:
    print(f"ERROR! Unexpected number of species found. Quitting...")
    sys.exit()

print(f"the total number of ectoparasites is {ecto_counter}")
print(f"the total number of endoparasites is {endo_counter}")
print(f"the total number of parasites is {ecto_counter+endo_counter}")
print(f"the total number of non-parasites is {non_counter}")

#read in the species tree file and store as a phylo object
sp_tree = Phylo.read("SP_tree_wasp.newick", "newick")
print(type(sp_tree))

# Define the color mapping for flighted and flightless
color_mapping = {
    'Endo': '#d55e00',
    'Ecto': '#cc79a7',
    'Non': '#009e73'
}

# Create a color map based on the Flighted_vs_flightless column
taxon_color_map = {row['Abbrev']: color_mapping[row['Character_state']] for idx, row in taxon_df.iterrows()}

# Function to apply color to taxon labels
def color_taxon_labels(clade, taxon_color_map):
    if clade.name in taxon_color_map:
        color = taxon_color_map[clade.name]
        clade.color = color
    if clade.is_terminal():
        clade.name = f"{clade.name}"
    for subclade in clade.clades:
        color_taxon_labels(subclade, taxon_color_map)

# Apply colors to the tree
color_taxon_labels(sp_tree.root, taxon_color_map)

# Draw the tree with colored labels
fig, ax = plt.subplots(figsize=(10, 14))
Phylo.draw(sp_tree, label_func=lambda x: x.name, do_show=False, axes=ax)

# Customize the labels with the specified colors
for label in ax.get_xticklabels():
    if label.get_text() in taxon_color_map:
        label.set_color(taxon_color_map[label.get_text()])

plt.savefig("labeled_sp_tree.pdf", format="pdf")

#Bonus: perform ancestral state reconstruction

# Map the states to the taxa in the tree
state_col = 'character_state'  # Replace with the name of the column containing character states in your CSV
sp_tree = ancestral_reconstruction(
    tree=sp_tree,
    data=taxon_df,
    columns=[state_col],  # List of columns for which to reconstruct states
    states_formats=['Sankoff'],  # Specify Sankoff algorithm; modify as needed
)

# Save the results
tree_output_path = 'SP_tree_wasp_ancestors.newick'
Phylo.write(sp_tree, tree_output_path, "newick")

# Optional: Visualize the tree
from pastml.visualization import plot_reconstruction
plot_reconstruction(sp_tree, output_file='ancestral_states_plot.html', state_col=state_col)

print(f"Ancestral state reconstruction completed. Results saved to {tree_output_path} and visualization to 'ancestral_states_plot.html'.")

