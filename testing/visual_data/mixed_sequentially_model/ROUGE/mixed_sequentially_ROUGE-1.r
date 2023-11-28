library(ggplot2)

# dataset names
dataset_names <- c("Attempts", "Goals", "Substitutions", "Offsides", "Cards", "Corners", "Fouls")

# iteration names - reflecting seven different models without refreshers
iteration_names <- c("Mixed Sequentially Model 1: Attempts", 
                     "Mixed Sequentially Model 2: Goals", 
                     "Mixed Sequentially Model 3: Subs", 
                     "Mixed Sequentially Model 4: Offsides", 
                     "Mixed Sequentially Model 5: Cards", 
                     "Mixed Sequentially Model 6: Corners", 
                     "Mixed Sequentially Model 7: Fouls")

# Create an empty data frame to store the model performance
model_performance <- data.frame(
  Iteration = factor(),
  Dataset = factor(),
  PerformanceMetric = numeric()
)

# Define the number of datasets to include in each iteration
datasets_per_iteration <- c(1, 2, 3, 4, 5, 6, 7)

# Populate the data frame with your data
for (i in 1:7) {
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
  geom_tile() +  # Use geom_tile for heatmap squares
  scale_fill_gradient(low = "blue", high = "red") +  # Color gradient for performance metric
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  labs(title = "Mixed Sequentially Model ROUGE-1 Heatmap",
       x = "Iteration",
       y = "Dataset",
       fill = "Performance Metric")

# Print the heatmap
print(heatmap)

# Save the heatmap
ggsave("mixed_sequentially_model_ROUGE_1_heatmap.png", plot = heatmap, width = 12, height = 6, dpi = 300)
