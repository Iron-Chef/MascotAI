import json
import random

# Load a jsonl dataset into a list
def load_dataset(filename):
    with open(filename, 'r') as f:
        return [json.loads(line) for line in f]

# Save a list into a jsonl dataset.
def save_dataset(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def main():
    # Load datasets
    attempts_dataset = load_dataset('dataset_attempts.jsonl')
    goals_dataset = load_dataset('dataset_goals.jsonl')
    substitutions_dataset = load_dataset('dataset_substitutions.jsonl')
    offsides_dataset = load_dataset('dataset_offsides.jsonl')
    cards_dataset = load_dataset('dataset_cards.jsonl')
    corners_dataset = load_dataset('dataset_corners.jsonl')
    fouls_dataset = load_dataset('dataset_fouls.jsonl')

    # Randomly sample from the datasets
    # Events are sequentially mixed in after the model has trained on them
    # Events are mixed in at fixed proportiongs
    # Note: No seeding is used, so samples will be different each time you run this
    attempts_sample = random.sample(attempts_dataset, 27000)
    save_dataset("training_datasets/mixed_sequentially_1_attempts.jsonl", attempts_sample)

    goals_sample = random.sample(goals_dataset, 27000)
    save_dataset("training_datasets/mixed_sequentially_2_goals.jsonl", attempts_sample + goals_sample)

    substitutions_sample = random.sample(substitutions_dataset, 9000)
    save_dataset("training_datasets/mixed_sequentially_3_subs.jsonl", attempts_sample + goals_sample + substitutions_sample)

    offsides_sample = random.sample(offsides_dataset, 9000)
    save_dataset("training_datasets/mixed_sequentially_4_offsides.jsonl", attempts_sample + goals_sample + substitutions_sample + offsides_sample)

    cards_sample = random.sample(cards_dataset, 18000)
    save_dataset("training_datasets/mixed_sequentially_5_cards.jsonl", attempts_sample + goals_sample + substitutions_sample + offsides_sample + cards_sample)

    corners_sample = random.sample(corners_dataset, 9000)
    save_dataset("training_datasets/mixed_sequentially_6_corners.jsonl", attempts_sample + goals_sample + substitutions_sample + offsides_sample + cards_sample + corners_sample)

    fouls_sample = random.sample(fouls_dataset, 9000)
    save_dataset("training_datasets/mixed_sequentially_7_fouls.jsonl", attempts_sample + goals_sample + substitutions_sample + offsides_sample + cards_sample + corners_sample + fouls_sample)

if __name__ == "__main__":
    main()
