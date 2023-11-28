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

# line graph
line_graph <- ggplot(data = model_performance, aes(x = Iteration, y = PerformanceMetric, group = Dataset, color = Dataset)) +
  geom_line() +
  geom_point() + 
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1, size = 8)) +
  labs(title = "Mixed Immediately Model BLEU Scores",
       x = "Iteration",
       y = "Average BLEU Score",
       color = "Dataset") + 
  scale_x_discrete(limits = iteration_names) +
  scale_color_brewer(palette = "Set1")

# Print the line graph
print(line_graph)

# Save the line graph
ggsave("mixed_immediately_model_BLEU.png", plot = line_graph, width = 12, height = 6, dpi = 600)
