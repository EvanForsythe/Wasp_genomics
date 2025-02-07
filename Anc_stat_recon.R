# Load necessary libraries
library(phytools)

# Step 1: Load the phylogenetic tree
tree_path <- "SP_tree_wasp.newick"  # Path to your Newick tree file
tree <- read.tree(tree_path)

# Step 2: Load the character state data
data_path <- "Wasp_character_states.csv"  # Path to your character states file
character_data <- read.csv(data_path)

# Match the abbreviations in the CSV to the tip labels in the tree
# Assuming the 'Abbrev' column corresponds to tip labels in the tree
rownames(character_data) <- character_data$Abbrev
character_states <- character_data$Character_state
names(character_states) <- rownames(character_data)

# Step 3: Convert character states to a factor (for discrete traits)
character_states <- as.factor(character_states)

# Step 4: Perform ancestral state reconstruction
# Using stochastic mapping with an equal-rates (ER) model
reconstructed <- make.simmap(tree, character_states, model = "ER", nsim = 100)

# Summarize the results
simmap_summary <- summary(reconstructed)
print(simmap_summary)

# Step 5: Visualize the results
# Plot the stochastic mapping results
output_plot_path <- "ancestral_states_plot.pdf"
pdf(output_plot_path)
plotSimmap(reconstructed, fsize = 0.8)
dev.off()
cat("Plot saved to:", output_plot_path, "\n")

# Step 6: Save the reconstructed tree
output_tree_path <- "SP_tree_wasp_ancestors.newick"
write.tree(tree, file = output_tree_path)
cat("Reconstructed tree saved to:", output_tree_path, "\n")
