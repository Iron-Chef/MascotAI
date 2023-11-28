library(ggplot2)

# dataset names
dataset_names <- c("Attempts", "Goals", "Substitutions", "Offsides", "Cards", "Corners", "Fouls")

# iteration names - reflecting five different models
iteration_names <- c("Mixed Immediately Model 1", "Mixed Sequentially Model 2", "Mixed Sequentially Model 3", "Mixed Sequentially Model 4", "Mixed Sequentially Model 5")

# Create an empty data frame to store the model performance
model_performance <- data.frame(
  Iteration = factor(),
  Dataset = factor(),
  PerformanceMetric = numeric()
)

# Populate the data frame with your data
for (i in 1:5) {  # Iterate over five models
  # Generate performance metrics for the datasets
  # Assuming each model is tested on all datasets
  performance_metrics <- runif(7, min = 0.5, max = 1)  # 7 datasets
  
  # Create iteration data for all datasets
  iteration_data <- data.frame(
    Iteration = factor(rep(iteration_names[i], 7), levels = iteration_names),  # Repeat for all datasets
    Dataset = factor(dataset_names, levels = dataset_names),
    PerformanceMetric = performance_metrics
  )
  
  # Combine the iteration data with the main data frame
  model_performance <- rbind(model_performance, iteration_data)
}

# Create the heatmap
heatmap <- ggplot(model_performance, aes(x = Iteration, y = Dataset, fill = PerformanceMetric)) +
  geom_tile(color = "white") +  # Add white lines to separate the tiles
  scale_fill_gradient(low = "blue", high = "red") +  # Use the same blue to red gradient for the performance metric
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  labs(title = "Mixed Immediately Model ROUGE-1 Heatmap",
       x = "Iteration",
       y = "Dataset",
       fill = "Performance Metric")

# Print the heatmap
print(heatmap)

# Save the heatmap
ggsave("mixed_immediatley_model_ROUGE_1_heatmap.png", plot = heatmap, width = 12, height = 6, dpi = 300)
