import json
import datetime
import os
import re
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from language_model import load_language_model

def split_event_prompts_and_references(dataset, event):

    prompts = []
    references = []

    with open(dataset, 'r') as f:
        data = [json.loads(line) for line in f]

    for obj in data:
        text = obj['text']

        if event == "Card":
            if "First yellow card" in text:
                pattern = re.compile("### Assistant: Booking")
            else:
                pattern = re.compile("### Assistant: Dismissal")
        else:
            pattern = re.compile(f"### Assistant: {event}")

        match = pattern.search(text)
        if match:
            split_point = match.end()
            prompt_text = text[:split_point]
            reference_text = text[split_point:]

            prompts.append(prompt_text)
            references.append(reference_text)
        else:
            print(f"No pattern matched for: {text}")

    return prompts, references

def model_tests(dataset, event, model_name):

    prompts, references = split_event_prompts_and_references(dataset, event)

    # Initalise the log variables
    formatted_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
    filename = f"{model_name} testing on {event} at {formatted_time}.txt"

    # Initalise the LLM and score variables
    llm = load_language_model(model_name)
    straight_comparison_score = 0
    bleu_score = 0
    rouge_score = 0
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_1_score = 0
    rouge_2_score = 0
    rouge_L_score = 0

    # Open the file for logging the tests
    with open(os.path.join("logs_tests", filename), 'w') as file:

        # Feed the prompts into an LLM
        for i in range(len(prompts)):
            llm_result = llm(prompts[i])
            print(str(i+1) + '. Testing')

            file.write("TEST NUMBER: " + str(i+1) + "\n\n")
            file.write(f"PROMPT: {prompts[i]} \n\n")
            file.write(f"EXPECTED ANSWER: {references[i]} \n\n")
            file.write(f"ACTUAL ANSWER: {llm_result} \n\n")

            # Straight comparison test 
            straight_comparison_outcome = False 

            if llm_result == references[i]:
                straight_comparison_score += 1
                straight_comparison_outcome = True

            file.write(f"STRAIGHT COMPARISON: {straight_comparison_outcome}\n")

            # Bleu test
            smoothie = SmoothingFunction().method4
            bleu_temp = round(sentence_bleu([references[i].split()], llm_result.split(), smoothing_function=smoothie), 2)
            bleu_score += bleu_temp
            file.write("BLEU SCORE: " + str(bleu_temp) + "\n")

            # Rouge tests
            scores = scorer.score(references[i], llm_result)

            rouge_1_temp = round(scores['rouge1'].fmeasure, 2)
            rouge_2_temp = round(scores['rouge2'].fmeasure, 2)
            rouge_L_temp = round(scores['rougeL'].fmeasure, 2)

            rouge_1_score += rouge_1_temp
            rouge_2_score += rouge_2_temp
            rouge_L_score += rouge_L_temp

            file.write("ROUGE-1 SCORE: " + str(rouge_1_temp) + "\n")
            file.write("ROUGE-2 SCORE: " + str(rouge_2_temp) + "\n")
            file.write("ROUGE-L SCORE: " + str(rouge_L_temp) + "\n\n")

        # Calculate average similarity and bleu scores
        #similarity_score = round(similarity_score / len(prompts), 2)
        bleu_score = round(bleu_score / len(prompts), 2)
        rouge_1_score = round (rouge_1_score / len(prompts), 2)
        rouge_2_score = round(rouge_2_score / len(prompts), 2)
        rouge_L_score = round(rouge_L_score / len(prompts), 2)

        # Print out scores 
        file.write(f"\n {event} FINAL STRAIGHT COMPARISON SCORE: {straight_comparison_score}\n")
        file.write(f"\n {event} FINAL BLEU SCORE: {bleu_score}\n")
        file.write(f"\n {event} FINAL ROUGE-1 SCORE: {rouge_1_score}\n")
        file.write(f"\n {event} FINAL ROUGE-2 SCORE: {rouge_2_score}\n")
        file.write(f"\n {event} FINAL ROUGE-L SCORE: {rouge_L_score}\n\n")

    scores = [straight_comparison_score, 
              bleu_score, 
              rouge_1_score, 
              rouge_2_score, 
              rouge_L_score
        ]

    return scores
