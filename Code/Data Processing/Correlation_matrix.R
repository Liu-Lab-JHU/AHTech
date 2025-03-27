“”“
This is an example on how to use R to generate the correlation matrix.
”“”

# Install and load the necessary packages
install.packages("corrplot")
install.packages("ggplot2")  

# Load necessary library
library(grDevices)
library(corrplot)
library(ggplot2)

# Create a color ramp function. Replace or omit if necessary.
start_color <- "#77A5D1"
end_color <- "#DC7775"
color_palette <- colorRampPalette(colors = c(start_color, "grey100",end_color))
# Generate a palette with, for example, 100 colors
palette <- color_palette(100)


# Load the dataset from a local CSV file
data <- read.csv("data_path") # Your data path

# Correlation analysis
cor_mat = cor(data[], method = "pearson") # Replace with "spearman" if necessary.

corrplot(
  cor_mat, 
  col=palette, 
  type="low", 
  methhod="color",
  number.cex=0.3, 
  tl.cex=0.3, 
  tl.col="black", 
  diag=FALSE
)
