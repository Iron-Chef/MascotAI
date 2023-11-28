import random
import json
import sys
sys.path.append("..")

# Read lines from a JSONL file into a list
def read_jsonl(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    return lines

# Write lines to a JSONL file
def write_jsonl(file_name, lines):
    with open(file_name, 'w') as f:
        f.writelines(lines)

# Read each dataset
attempts_dataset = read_jsonl('../dataset_attempts.jsonl')
goals_dataset = read_jsonl('../dataset_goals.jsonl')
substitutions_dataset = read_jsonl('../dataset_substitutions.jsonl')
offsides_dataset = read_jsonl('../dataset_offsides.jsonl')
cards_dataset = read_jsonl('../dataset_cards.jsonl')
corners_dataset = read_jsonl('../dataset_corners.jsonl')
fouls_dataset = read_jsonl('../dataset_fouls.jsonl')

# Randomly sample lines from each dataset
# The ratio should be 3:3:1:1:2:1:1 (in order)
# 27000 is used as the largest sample size becuase the total size of the goals dataset is only 27k
attempts_sample = random.sample(attempts_dataset, 27000)
goals_sample = random.sample(goals_dataset, 27000)
substitutions_sample = random.sample(substitutions_dataset, 9000)
offsides_sample = random.sample(offsides_dataset, 9000)
cards_sample = random.sample(cards_dataset, 18000)
corners_sample = random.sample(corners_dataset, 9000)
fouls_sample = random.sample(fouls_dataset, 9000)

# Combine and shuffle the lines
combined_dataset = attempts_sample + goals_sample + substitutions_sample + offsides_sample + cards_sample + corners_sample + fouls_sample
random.shuffle(combined_dataset)

# Write to a new JSONL file
write_jsonl('../REFRESH_attempts_goals_subs_offsides_cards_corners_fouls.jsonl', combined_dataset)