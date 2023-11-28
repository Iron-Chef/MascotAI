import json
import re

def split_event_prompts_and_references(dataset):
    prompts = []
    references = []

    with open(dataset, 'r') as f:
        data = [json.loads(line) for line in f]

    for obj in data:
        text = obj['text']
        
        match = re.search(r'Event:\s*([^\.]+)\.', text)
        if match:
            event = match.group(1).strip()
        else:
            print('No match found')

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