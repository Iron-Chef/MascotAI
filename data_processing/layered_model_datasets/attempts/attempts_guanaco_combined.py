import csv
import json
import re
import sys
sys.path.append("..")
from character_rendering import correct_player_names
  
# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:

    reader_obj = csv.reader(file_obj)

    # Iterate over dataset
    with open('dataset_attempts.jsonl', 'w') as f:

        for row in reader_obj:

            # Check for attempt events
            if row[5] == "1" and row[16] == "0":

                # Starting building the prompt
                event = "Attempt"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                assister = ""
                if row[11] != "NA":
                    assister = row[11]
                attempt_result = ""

                # Assist Method
                assist_method_dict = {
                    "0": "",
                    "1": "Pass",
                    "2": "Cross",
                    "3": "Headed pass",
                    "4": "Through ball"
                }
                assist_method = assist_method_dict[row[19]]

                # Attempt Placement
                attempt_placement_dict = {
                    "NA": "",
                    "1": "Bit too high",
                    "2": "Blocked",
                    "3": "Bottom left corner",
                    "4": "Bottom right corner",
                    "5": "Centre of the goal",
                    "6": "High and wide",
                    "7": "Hits the bar",
                    "8": "Misses to the left",
                    "9": "Misses to the right",
                    "10": "Too high",
                    "11": "Top centre of the goal",
                    "12": "Top left corner",
                    "13": "Top right corner"
                }
                attempt_placement = attempt_placement_dict[row[14]]

                #Pitch Position
                pitch_position_dict = {
                    "NA": "",                   
                    "1": "Attacking half",
                    "2": "Defensive half",
                    "3": "Centre of the box",
                    "4": "Left wing",
                    "5": "Right wing",
                    "6": "Difficult angle and long range",
                    "7": "Difficult angle on the left",
                    "8": "Difficult angle on the right",
                    "9": "Left side of the box",
                    "10": "Left side of the six yard box",
                    "11": "Right side of the box",
                    "12": "Right side of the six yard box",
                    "13": "Very close range",
                    "14": "Penalty spot",
                    "15": "Outside the box",
                    "16": "Long range",
                    "17": "More than 35 yards",
                    "18": "More than 40 yards",
                    "19": "Not recorded"
                } 
                pitch_position = pitch_position_dict[row[17]]

                # Attempt following
                attempt_following_dict = {
                    "NA": "",
                    "1": "Open play",
                    "2": "Set piece",
                    "3": "Corner",
                    "4": "Free kick"
                }
                attempt_following = attempt_following_dict[row[20]]

                # Foot
                foot_dict = {
                    "NA": "",
                    "1": "right foot",
                    "2": "left foot",
                    "3": "head"
                }
                foot = foot_dict[row[18]]

                # Shot outcome
                shot_outcome_dict = {
                    "NA": "",
                    "1": "Saved",
                    "2": "Missed",
                    "3": "Blocked",
                    "4": "Hit the bar"
                }
                attempt_result = shot_outcome_dict[row[15]]

                # Attempt result conditionals
                if "hits the right post" in row[4]:
                    attempt_placement = "Hits the right post"
                elif "hits the left post" in row[4]:
                    attempt_placement = "Hits the left post"

                # The acutal prompt
                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assister: {assister}. ### Assist Method: {assist_method}. ### Attempt Result: {attempt_result}. ### Foot: {foot}. ### Pitch Position: {pitch_position}. ### Attempt Placement: {attempt_placement}. ### Attempt Following: {attempt_following}. ### Assistant: {row[4]} "
                }

                event_dict["text"] += correct_player_names(row[4], player, assister)

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:

    reader_obj = csv.reader(file_obj)
    bbc_attempts_total = 0

    with open('dataset_attempts.jsonl', 'a') as f:
        for row in reader_obj:

            if row[14] == "Attempt":
                event = row[14]
                time = row[6]
                event_team = row[15]
                opponent_team = row[16]
                player = row[17]
                assister = ""
                assist_method = row[22]
                attempt_result = ""
                foot = row[24]
                pitch_position = row[19]
                attempt_placement = row[20]
                attempt_following = ""

                # Attempt result conditionals
                if "hits the right post" in row[12]:
                    attempt_result = "Hits the right post"
                elif "hits the left post" in row[12]:
                    attempt_result = "Hits the left post"
                else:
                    attempt_result = row[18]

                # Assister conditionals
                match = re.search(r'Assisted by (.*?) with', row[12])
                if match:
                   assister = match.group(1).strip()

                if "Assisted by" in row[12] and len(assister) == 0:
                    match = re.search(r'Assisted by (.*?)[.]', row[12])
                    if match:
                        assister = match.group(1).strip()
                
                if "Assisted by" in row[12] and "following" in assister:
                    match = re.search(r'Assisted by (.*?) following', row[12])
                    if match:
                        assister = match.group(1).strip()

                # Assist following conditionals
                if len(row[21]) != 0:
                    attempt_following = row[21]
                elif "set piece" in row[12]:
                    attempt_following = "Set Piece"
                else:
                    attempt_following = row[23]

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assister: {assister}. ### Assist Method: {assist_method}. ### Attempt Result: {attempt_result}. ### Foot: {foot}. ### Pitch Position: {pitch_position}. ### Attempt Placement: {attempt_placement}. ### Attempt Following: {attempt_following}. ### Assistant: "
                }

                event_dict["text"] += correct_player_names(row[12], row[17], assister)

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')