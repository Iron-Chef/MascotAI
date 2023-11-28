library(ggplot2)
library(tidyr)

# Define the data in a data frame
data <- data.frame(
  Iteration = rep(c("Layered Model 1: Attempts",
                    "Layered Model 2: Goals", 
                    "Layered Model 3: Subs", 
                    "Layered Model 4: Rehearsal One", 
                    "Layered Model 5: Offsides", 
                    "Layered Model 6: Rehearsal Two", 
                    "Layered Model 7: Cards", 
                    "Layered Model 8: Corners", 
                    "Layered Model 9: Rehearsal Three", 
                    "Layered Model 10: Fouls", 
                    "Layered Model 11: Rehearsal Four"), 
                  times = c(1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7)),

  Dataset = rep(c("Attempts", "Goals", "Subs", "Offsides", "Cards", "Corners", "Fouls"), 
                times = c(1, 2, 3, 4, 5, 6, 7)),

  PerformanceMetric = c(64, # Attempts
                        23, 67, # Goals
                        18, 53, 98, # Subs
                        71, 70, 95, # Rehearsal One
                        67, 65, 6, 85, # Offsides
                        70, 70, 94, 88, # Rehearsal Two
                        69, 65, 84, 73, 72, # Cards
                        73, 63, 87, 88, 72, 99, # Corners
                        72, 70, 94, 88, 72, 99, # Rehearsal Three
                        65, 63, 96, 77, 73, 99, 99, # Fouls
                        73, 70, 93, 86, 74, 99, 100 # Rehearsal Four
  ) 
)


# Transform data to long format
long_data <- gather(data, key = "Metric", value = "Score", -Iteration, -Dataset)

# Create the line graph
line_graph <- ggplot(long_data, aes(x = Iteration, y = Score, group = Dataset, color = Dataset)) +
  geom_line() +
  geom_point() + # Optional: Adds points to the line graph
  scale_y_continuous(limits = c(0, 100)) + # Set y-axis limits
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  labs(title = "Layered Model Comparison Performance",
       x = "Iteration",
       y = "Comparison Score")

# Save the line graph
ggsave("layered_model_performance_line_graph.png", plot = line_graph, width = 12, height = 6, dpi = 300)
