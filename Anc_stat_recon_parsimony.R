# Load necessary libraries
library(ape)
library(phangorn)

# Step 1: Load the phylogenetic tree
tree_path <- "SP_tree_wasp.newick"  # Path to your Newick tree file
tree <- read.tree(tree_path)

# Step 2: Load the character state data
data_path <- "Wasp_character_states.csv"  # Path to your character states file
character_data <- read.csv(data_path)

# Match the abbreviations in the CSV to the tip labels in the tree
character_data <- character_data[match(tree$tip.label, character_data$Abbrev), ]

# Check for missing matches
if (any(is.na(character_data$Abbrev))) {
  stop("Some tip labels in the tree do not match abbreviations in the character data.")
}

# Step 3: Prepare character data for analysis
# Convert the character states to a named factor
character_states <- setNames(as.factor(character_data$Character_state), character_data$Abbrev)

# Define state colors
state_colors <- setNames(c("red", "blue", "green"), levels(character_states))  # Customize as needed

# Step 4: Perform ancestral state reconstruction with ace()
# Use ace() for discrete traits
reconstruction <- ace(character_states, tree, type = "discrete", model = "ARD") #ER. SYM, ARD

# Debugging: Print the reconstruction results
print("Ancestral state reconstruction results:")
print(reconstruction)

# Step 5: Visualize the reconstructed states with tip label colors and a legend
output_plot_path <- "ACE_ancestral_states_with_tip_colors_and_legend.pdf"
pdf(output_plot_path)

# Plot the tree
plot(tree, show.tip.label = TRUE, cex = 0.8)

# Add tip labels with colors based on character states
tip_colors <- state_colors[character_states[tree$tip.label]]
tiplabels(pch = 19, col = tip_colors, cex = 1)

# Add pie charts for ancestral states
nodelabels(pie = reconstruction$lik.anc, piecol = state_colors, cex = 0.8)

# Add a legend
legend("topleft", legend = names(state_colors), fill = state_colors, title = "States", cex = 0.8, bty = "n")

dev.off()
cat("Ancestral states plot with tip colors and legend saved to:", output_plot_path, "\n")

# Step 6: Save the reconstructed tree
output_tree_path <- "SP_tree_wasp_ACE_ancestors_with_tip_colors_and_legend.newick"
write.tree(tree, file = output_tree_path)
cat("Tree with ACE ancestral states, tip colors, and legend saved to:", output_tree_path, "\n")
