import datetime
import os
from dataset_creator import create_test_dataset
from model_testing import model_tests

print("Welcome! These are your choices: \n")
print("[1] Layered Models \n")
print("[2] Mixed Sequentially Models \n")
print("[3] Mixed Immediately Models \n\n")

model_choice = input("Please select your choice: ")

# Utility function to write the models scores to the log file
def save_scores(event_name, score_list, file):

    # Save the scores to a log file
    comparison_score = f"{event_name} Straight comparison score = {score_list[0]}\n"
    #similarity_score = f"{event_name} Similarity score = {score_list[1]}.\n"
    bleu_score = f"{event_name} BLEU score = {score_list[1]}\n"
    rouge_1_score = f"{event_name} ROUGE-1 score = {score_list[2]}\n"
    rouge_2_score = f"{event_name} ROUGE-2 score = {score_list[3]}\n"
    rouge_L_score = f"{event_name} ROUGE-L score = {score_list[4]}\n"

    scores_list = [comparison_score, 
                   #similarity_score, 
                   bleu_score, 
                   rouge_1_score, 
                   rouge_2_score, 
                   rouge_L_score
                ]
    for score in scores_list:
        file.write(score)

# test datasets and key event word
# event key words are used to split the jsonl objects into prompts and references
test_datasets = [
    ('test_datasets/attempts_test_dataset.jsonl', 'Attempt'),
    ('test_datasets/goals_test_dataset.jsonl', 'Goal'),
    ('test_datasets/substitutions_test_dataset.jsonl', 'Substitution'),
    ('test_datasets/offsides_test_dataset.jsonl', 'Offside'),
    ('test_datasets/cards_test_dataset.jsonl', 'Card'),
    ('test_datasets/corners_test_dataset.jsonl', 'Corner'),
    ('test_datasets/fouls_test_dataset.jsonl', 'Foul')
    ]

#################### LAYERED MODELS ####################

layered_models=[
    'layered_model_1_Attempts',
    'layered_model_2_Goals',
    'layered_model_3_Subs',
    'layered_model_4_REFRESH_ONE',
    'layered_model_5_Offsides',
    'layered_model_6_REFRESH_TWO',
    'layered_model_7_Cards',
    'layered_model_8_Corners',
    'layered_model_9_REFRESH_THREE',
    'layered_model_10_Fouls',
    'layered_model_11_REFRESH_FOUR',
    ]
    

if model_choice == '1':

    print("Testing layered models \n\n")
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d-%m-%y %H:%M")
    filename = f"log_{formatted_time}.txt"
    refresh_count = 0 # Ensures the REFRESH models don't increment the loop counter

    with open(os.path.join("layered_model_scores", filename), 'w') as file:

        for model_index, model in enumerate(layered_models):

            if "REFRESH" in model:
                dataset_range = range(model_index - refresh_count)
                refresh_count += 1
            else:
                dataset_range = range((model_index + 1) - refresh_count)

            for dataset_index in dataset_range:

                test_dataset, event = test_datasets[dataset_index]
                print(f"Testing {model} on {test_dataset}")
                
                scores = model_tests(test_dataset, event, model)
                file.write(f"{model}\n")
                
                save_scores(event, scores, file)
                file.write("\n\n")

#################### MIXED SEQUENTIALLY MODELS ###################

mixed_sequentially_models=[
    'mixed_sequentially_1_Attempts',
    'mixed_sequentially_2_Goals',
    'mixed_sequentially_3_Subs',
    'mixed_sequentially_4_Offsides',
    'mixed_sequentially_5_Cards',
    'mixed_sequentially_6_Corners',
    'mixed_sequentially_7_Fouls',
    ] 

if model_choice == '2':

    print("Testing mixed sequentially models")
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d-%m-%y %H:%M")
    filename = f"log_{formatted_time}.txt"

    with open(os.path.join("mixed_sequentially_model_scores", filename), 'w') as file:

        for model_index, model in enumerate(mixed_sequentially_models):

            for dataset_index in range(model_index + 1):

                test_dataset, event = test_datasets[dataset_index]
                print(f"Testing {model} on {test_dataset}")
                
                scores = model_tests(test_dataset, event, model)
                file.write(f"{model}\n")
                
                save_scores(event, scores, file)
                file.write("\n\n")

#################### MIXED IMMEDIATELY MODELS ###################


mixed_immediately_models=[
    'mixed_immediately_1',
    'mixed_immediately_2',
    'mixed_immediately_3',
    'mixed_immediately_4',
    'mixed_immediately_5',
    ]  

if model_choice == '3':

    print("Testing mixed immediately models \n\n")
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d-%m-%y %H:%M")
    filename = f"log_{formatted_time}.txt"

    with open(os.path.join("mixed_immediately_model_scores", filename), 'w') as file:

        for model in mixed_immediately_models:

            for test_dataset, event in test_datasets:

                print(f"Testing {model} on {test_dataset}")
                
                scores = model_tests(test_dataset, event, model)
                file.write(f"{model}\n")
                
                save_scores(event, scores, file)
                file.write("\n\n")
