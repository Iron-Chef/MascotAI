library(ggplot2)
library(tidyr)

# Define the data in a data frame
data <- data.frame(
  Iteration = factor(rep(c("Layered Model 1: Attempts", "Layered Model 2: Goals", "Layered Model 3: Subs", 
                    "Layered Model 4: Rehearsal  One", "Layered Model 5: Offsides", "Layered Model 6: Rehearsal  Two", "Layered Model 7: Cards", "Layered Model 8: Corners", "Layered Model 9: Rehearsal  Three", "Layered Model 10: Fouls", "Layered Model 11: Rehearsal  Four"), each = 7),
              levels = c("Layered Model 1: Attempts", "Layered Model 2: Goals", "Layered Model 3: Subs", 
                               "Layered Model 4: Rehearsal  One", "Layered Model 5: Offsides", "Layered Model 6: Rehearsal  Two", "Layered Model 7: Cards", "Layered Model 8: Corners", "Layered Model 9: Rehearsal  Three", "Layered Model 10: Fouls", "Layered Model 11: Rehearsal  Four")),

  Dataset = factor(rep(c("Attempts", "Goals", "Subs", "Offsides", "Cards", "Corners", "Fouls"), times = 11),
                    levels = c("Attempts", "Goals", "Subs", "Offsides", "Cards", "Corners", "Fouls")),

  PerformanceMetric = c(64, NA, NA, NA, NA, NA, NA, # Attempts
                        23, 67, NA, NA, NA, NA, NA, # Goals
                        18, 53, 98, NA, NA, NA, NA, # Subs
                        71, 70, 95, NA, NA, NA, NA, # Rehearsal 1
                        67, 65,  6, 85, NA, NA, NA, # Offsides
                        70, 70, 94, 88, NA, NA, NA, # Rehearsal 2
                        69, 65, 84, 73, 72, NA, NA, # Cards
                        73, 62, 87, 88, 72, 99, NA, # Corners
                        72, 70, 94, 88, 72, 99, NA, # Rehearsal 3
                        65, 63, 96, 77, 73, 99, 99, # Fouls
                        73, 70, 93, 86, 74, 99, 100 # Rehearsal 4
  ) 
)

# Transform data to long format
long_data <- gather(data, key = "Metric", value = "Score", -Iteration, -Dataset)

# Create the heatmap using the 'Reds' color palette
heatmap <- ggplot(long_data, aes(x = Iteration, y = Dataset, fill = Score)) +
  geom_tile(color = "white") +
  scale_fill_distiller(palette = "Reds", limits = c(0, 100), na.value = "#FFFFFF",
                       direction = 1, labels = seq(0, 100, by = 10), breaks = seq(0, 100, by = 10)) +
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  labs(title = "Layered Model Performance Heatmap",
       x = "Iteration",
       y = "Dataset",
       fill = "Performance Metric")


# Save the heatmap
ggsave("layered_model_performance_heatmap.png", plot = heatmap, width = 12, height = 6, dpi = 300)
