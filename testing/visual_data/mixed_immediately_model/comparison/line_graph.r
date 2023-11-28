library(ggplot2)
library(tidyr)

# Define the data in a data frame
data <- data.frame(
  Iteration = factor(rep(c("Mixed Immediately Model 1", "Mixed Immediately Model 2", "Mixed Immediately Model 3", "Mixed Immediately Model 4", "Mixed Immediately Model 5"), times = 7)),

  Dataset = factor(rep(c("Attempts", "Goals", "Subs", "Offsides", "Cards", "Corners", "Fouls"), each = 5)),

  PerformanceMetric = c(59, 64, 68, 71, 73, # Attempts
                        62, 61, 66, 66, 63, # Goals
                        81, 88, 96, 94, 94, # Subs
                        73, 87, 83, 87, 86, # Offsides
                        75, 68, 72, 69, 71, # Cards
                        99, 99, 99, 99, 99, # Corners
                        54, 98, 98, 100, 100  # Fouls
  ) 
)

# Transform data to long format
long_data <- gather(data, key = "Metric", value = "Score", -Iteration, -Dataset)

# Create the line graph
line_graph <- ggplot(long_data, aes(x = Iteration, y = Score, group = Dataset, color = Dataset)) +
  geom_line() +
  geom_point() + # Optional: Adds points to the line graph
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  labs(title = "Mixed Immediately Model Comparison Performance",
       x = "Iteration",
       y = "Straight comparison score") +
  scale_y_continuous(limits = c(0, 100)) # Set y-axis limits

# Save the line graph
ggsave("mixed_immediately_model_performance_line_graph.png", plot = line_graph, width = 12, height = 6, dpi = 300)
