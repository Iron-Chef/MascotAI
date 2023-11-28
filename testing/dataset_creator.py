import json
import random
import os

def create_test_dataset(input_file, output_file, event):
    random.seed(14)

    with open(input_file, 'r') as f:
        data = [json.loads(line) for line in f]

    # Filter the data to only include samples with the "### Assistant:" substring
    if event == "Cards":
        filtered_data = [obj for obj in data if "### Assistant:" in obj['text']]    

    else:
        filtered_data = [obj for obj in data if f"### Assistant: {event}" in obj['text']]

    test_samples = random.sample(filtered_data, 100)

    output_file_path = os.path.join('test_datasets', output_file)

    with open(output_file_path, 'w') as f:
        for sample in test_samples:
            f.write(json.dumps(sample) + '\n')

    print(f"Test dataset saved as {output_file_path}")

