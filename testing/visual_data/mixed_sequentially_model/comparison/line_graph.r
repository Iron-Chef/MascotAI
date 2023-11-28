library(ggplot2)
library(tidyr)

# Define the data in a data frame
data <- data.frame(
  Iteration = factor(rep(c("Mixed Sequentially Model 1: Attempts", "Mixed Sequentially Model 2: Goals", "Mixed Sequentially Model 3: Subs", "Mixed Sequentially Model 4: Offsides", "Mixed Sequentially Model 5: Cards", "Mixed Sequentially Model 6: Corners", "Mixed Sequentially Model 7: Fouls"), each = 7),
              levels = c("Mixed Sequentially Model 1: Attempts", "Mixed Sequentially Model 2: Goals", "Mixed Sequentially Model 3: Subs", "Mixed Sequentially Model 4: Offsides", "Mixed Sequentially Model 5: Cards", "Mixed Sequentially Model 6: Corners", "Mixed Sequentially Model 7: Fouls")),

  Dataset = factor(rep(c("Attempts", "Goals", "Subs", "Offsides", "Cards", "Corners", "Fouls")),
                    levels = c("Attempts", "Goals", "Subs", "Offsides", "Cards", "Corners", "Fouls")),

  PerformanceMetric = c(49, NA, NA, NA, NA, NA, NA, # Attempts
                        65, 70, NA, NA, NA, NA, NA, # Goals
                        66, 69, 78, NA, NA, NA, NA, # Subs
                        63, 73, 85, 88, NA, NA, NA, # Offsides
                        71, 65, 86, 85, 72, NA, NA, # Cards
                        71, 70, 92, 88, 71, 98, NA, # Corners
                        65, 32, 90, 88, 72, 98, 100 # Fouls
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
  labs(title = "Mixed Sequentially Model Comparison Performance",
       x = "Iteration",
       y = "Sraight comparison score")

# Save the line graph
ggsave("mixed_sequentially_model_performance_line_graph.png", plot = line_graph, width = 12, height = 6, dpi = 300)