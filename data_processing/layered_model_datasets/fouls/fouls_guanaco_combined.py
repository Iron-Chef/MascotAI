import csv
import json
import sys
sys.path.append("..")

from character_rendering import correct_player_names_fouls
  
# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    european_fouls_total = 0

    # Iterate over each row in the csv 
    with open('./dataset_fouls.jsonl', 'w') as f:
        for row in reader_obj:

            # Check for foul events
            if row[5] == "3":
                event = "Foul"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                
                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_fouls(row[4], player)

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    bbc_fouls_total = 0

    with open('./dataset_fouls.jsonl', 'a') as f:
        for row in reader_obj:

            if row[14] == "Foul conceded":
                event = "foul"
                time = row[6]
                event_team = row[15]
                opponent_team = row[16]
                player = row[17]

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_fouls(row[12], player)
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')