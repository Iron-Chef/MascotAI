library(ggplot2)

# dataset names
dataset_names <- c("Attempts", "Goals", "Substitutions", "Offsides", "Cards", "Corners", "Fouls")

# iteration names
iteration_names <- c("Layered Model 1: Attempts", "Layered Model 2: Goals", "Layered Model 3: Subs", "Layered Model 4: Refresh One", "Layered Model 5: Offsides", "Layered Model 6: Refresh Two", "Layered Model 7: Cards", "Layered Model 8: Corners", "Layered Model 9: Refresh Four", "Layered Model 10: Fouls", "Layered Model 11: Refresh Four")

model_performance <- data.frame(
  Iteration = factor(),
  Dataset = factor(),
  PerformanceMetric = numeric()
)

# number of datasets to include in each iteration
datasets_per_iteration <- c(1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7)

for (i in 1:11) {
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


# line graph
line_graph <- ggplot(data = model_performance, aes(x = Iteration, y = PerformanceMetric, group = Dataset, color = Dataset)) +
  geom_line() +
  geom_point() + 
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1, size = 8)) +
  labs(title = "Layered Model BLEU Scores ",
       x = "Iteration",
       y = "Average BLEU Score",
       color = "Dataset") + 
  scale_x_discrete(limits = iteration_names) +
  scale_color_brewer(palette = "Set1")


print(line_graph)

ggsave("layered_model_BLEU.png", plot = line_graph, width = 12, height = 6, dpi = 600)
