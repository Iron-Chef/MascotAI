import csv
import json
import sys
sys.path.append("..")
from character_rendering import correct_player_names_offsides
  
# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:

    reader_obj = csv.reader(file_obj)
    european_offsides_total = 0

    # Iterate over each row in the csv 
    with open('./dataset_offside.jsonl', 'w') as f:
        for row in reader_obj:

            # Check for offside events
            if row[5] == "9":
                event = "Offside"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                passer = row[11]
                offside_player = row[10]

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Passer: {passer}. ### Offside Player: {offside_player}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_offsides(row[4], passer, offside_player)

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    bbc_offsides_total = 0

    with open('./dataset_offside.jsonl', 'a') as f:
        for row in reader_obj:

            if row[14] == "Offside - Played Ball":
                event = "Offside"
                time = row[6]
                event_team = row[15]
                opponent_team = row[16]
                passer = row[17]

            if row[14] == "Offside - Player Offside":

                offside_player = row[17]

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {row[6]}. ### Event Team: {event_team}. ### Opponent Team: {row[16]}. ### Passer: {passer}. ### Offside Player: {offside_player}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_offsides(row[12], passer, offside_player)
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')