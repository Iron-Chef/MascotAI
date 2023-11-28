import json
import random

# Load a jsonl dataset into a list.
def load_dataset(filename):
    with open(filename, 'r') as f:
        return [json.loads(line) for line in f]

#Save a list into a jsonl dataset
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

    # Create 10 datasets with a fixed proportion of events
    # Each dataset is different to the one before, combatting overfitting
    for i in range(1, 11):
        attempts_sample = random.sample(attempts_dataset, 27000)
        goals_sample = random.sample(goals_dataset, 27000)
        substitutions_sample = random.sample(substitutions_dataset, 9000)
        offsides_sample = random.sample(offsides_dataset, 9000)
        cards_sample = random.sample(cards_dataset, 18000)
        corners_sample = random.sample(corners_dataset, 9000)
        fouls_sample = random.sample(fouls_dataset, 9000)

        save_dataset(f"training_datasets/mixed_immediately_{i}.jsonl", 
                                                                    attempts_sample + 
                                                                    goals_sample + 
                                                                    substitutions_sample + 
                                                                    offsides_sample + 
                                                                    cards_sample + 
                                                                    corners_sample + 
                                                                    fouls_sample
                                                                    )

if __name__ == "__main__":
    main()
