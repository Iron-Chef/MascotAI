import csv
import json
import sys
sys.path.append("..")
from character_rendering import correct_player_names_corners

# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    european_corners_total = 0
    
    # Iterate over each row in the csv 
    with open('./dataset_corners.jsonl', 'w') as f:
        for row in reader_obj:

            # Check for corner events
            if row[5] == "2":
                event = "Corner"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                conceded_by = row[10]

                # Keeps events uniform
                if conceded_by == "NA":
                   continue

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Conceded by: {conceded_by}. ### Assistant: "
                }
                event_dict["text"] += correct_player_names_corners(row[4], conceded_by)

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    bbc_corners_total = 0

    with open('./dataset_corners.jsonl', 'a') as f:
        for row in reader_obj:

            if row[14] == "Corner conceded":
                event = "Corner"
                time = row[6]
                conceded_by = row[17]
                event_team = row[16]
                opponent_team = row[15]

                if len(row[15]) == 0:
                    parts = row[12].split("Corner, ", 1)
                    event_team = parts[1]
                    event_team = event_team.replace(".","")


                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Conceded by: {conceded_by}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names_corners(row[12], conceded_by)
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')
