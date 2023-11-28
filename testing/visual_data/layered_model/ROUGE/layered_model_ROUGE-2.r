library(ggplot2)

# dataset names
dataset_names <- c("Attempts", "Goals", "Substitutions", "Offsides", "Cards", "Corners", "Fouls")

# iteration names - including refresher rounds
iteration_names <- c("Layered Model 1: Attempts", "Layered Model 2: Goals", "Layered Model 3: Subs", 
                     "Layered Model 4: Refresh One", "Layered Model 5: Offsides", "Layered Model 6: Refresh  Two", "Layered Model 7: Cards", "Layered Model 8: Corners", "Layered Model 9: Refresh Three", "Layered Model 7: Fouls", "Layered Model 11: Refresh Four ")

# Create an empty data frame to store the model performance
model_performance <- data.frame(
  Iteration = factor(),
  Dataset = factor(),
  PerformanceMetric = numeric()
)

# number of datasets to include in each iteration, including refreshers
datasets_per_iteration <- c(1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7)

for (i in 1:length(iteration_names)) {
  # Get the number of datasets for this iteration
  num_datasets <- datasets_per_iteration[i]
  
  # Generate performance metrics for the datasets
  performance_metrics <- runif(num_datasets, min = 0.5, max = 1)
  
  # Create iteration data for the current number of datasets
  iteration_data <- data.frame(
    Iteration = factor(rep(iteration_names[i], num_datasets), levels = iteration_names),
    Dataset = factor(dataset_names[1:num_datasets], levels = dataset_names),
    PerformanceMetric = performance_metrics
  )
  
  # Combine the iteration data with the main data frame
  model_performance <- rbind(model_performance, iteration_data)
}

# Create the heatmap
heatmap <- ggplot(model_performance, aes(x = Iteration, y = Dataset, fill = PerformanceMetric)) +
  geom_tile(color = "white") + # Add white lines to separate the tiles
  scale_fill_gradient(low = "blue", high = "red") + # Define the color gradient for the fill
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  labs(title = "Layered Model ROUGE-2 Heatmap",
       x = "Iteration",
       y = "Dataset",
       fill = "Performance Metric")

# Print the heatmap
print(heatmap)

# Save the heatmap
ggsave("layered_model_performance_ROUGE_2_heatmap.png", plot = heatmap, width = 12, height = 6, dpi = 300)
