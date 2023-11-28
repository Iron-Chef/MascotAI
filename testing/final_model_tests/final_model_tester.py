import datetime
import os
import sys
sys.path.append("..")

from event_splitter import split_event_prompts_and_references
from language_model import load_language_model


models = [
    'layered_model_11_REFRESH_FOUR',
    'mixed_sequentially_7_Fouls',
    'mixed_immediately_5',
]

# Generate the prompts and references from the dataset
prompts, references = (split_event_prompts_and_references('full_match_dataset.jsonl'))

# Loop through the models
for model in models:

    # Initalise the log variables
    formatted_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
    filename = f"{model} at {formatted_time}.txt"

    # Load the model from HuggingFace repo
    llm = load_language_model(model)

    # Loop through the prompts and feed them to the LLM
    with open(os.path.join("test_runs", filename), 'w') as file:
        for i in range(len(prompts)):
            llm_result = llm(prompts[i])
            file.write(f"TEST NUMBER: {i+1}\n")
            file.write(f"PROMPT: {prompts[i]}\n\n")
            file.write(f"REFERENCE: {references[i]}\n")
            file.write(f"ANSWER: {llm_result}\n\n")

            if llm_result == references[i]:
                file.write('Comparison = TRUE\n\n\n')
            else:
                file.write('Comparison = FALSE\n\n\n')

            print(f'Event: {i+1}. Testing')

    
