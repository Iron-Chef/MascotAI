import csv
import json
import re
import sys
sys.path.append("..")
from character_rendering import correct_player_names_substitutions
  
# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    european_subs_total = 0

    # Iterate over each row in the csv 
    with open('./dataset_substitutions.jsonl', 'w') as f:
        for row in reader_obj:

            # Check for substitution events
            if row[5] == "7":
                event = "Substitution"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player_on = row[12]
                player_off = row[13]
                reason = ""

                # Finding the reason
                if "because of an" in row[4]: 
                    parts = row[4].split("because of an", 1)
                    reason = parts[1].strip()
                    reason = reason.replace(".","")

                # Fixing errors in the dataset
                assistant_answer = re.sub(r'(Substitution\s+)+', 'Substitution ', row[4])
                assistant_answer = re.sub(r'Substitution(.+?)Substitution', 'Substitution', assistant_answer)

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player On: {player_on}. ### Player Off: {player_off}. ### Reason: {reason}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_substitutions(assistant_answer, player_on, player_off)

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    bbc_subs_total = 0

    with open('./dataset_substitutions.jsonl', 'a') as f:
        for row in reader_obj:

            if row[14] == "Substition - Player On":
                event = "Substitution"
                player_on = row[17]
                reason = ""

                parts = row[12].split("replaces", 1)
                parts2 = parts[1].split("because", 1)
                player_off = parts2[0].strip()

                if "because of an" in row[12]: 
                    parts = row[12].split("because of an", 1)
                    reason = parts[1].strip()
                    reason = reason.replace(".","")

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {row[6]}. ### Event Team: {row[15]}. ### Opponent Team: {row[16]}. ### Player On: {player_on}. ### Player Off: {player_off}. ### Reason: {reason}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_substitutions(row[12], player_on, player_off)

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')