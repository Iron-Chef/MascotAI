import csv
import json
import re
import sys
sys.path.append("..")
from character_rendering import correct_player_names
  
# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:

    reader_obj = csv.reader(file_obj)
    european_goals_total = 0

    # Iterate over each row in the csv 
    with open('dataset_goals.jsonl', 'w') as f:
        for row in reader_obj:

            # Check for goal events
            if row[16] == "1":
                event = "Goal"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                assist = ""

                if row[11] != "NA":
                    assist = row[11]

                assist_method_dict = {
                    "0": "",
                    "1": "Pass",
                    "2": "Cross",
                    "3": "Headed pass",
                    "4": "Through ball"
                }
                assist_method = assist_method_dict[row[19]]

                goal_placement_dict = {
                    "NA": "",
                    "3": "Bottom left corner",
                    "4": "Bottom right corner",
                    "5": "Centre of the goal",
                    "11": "Top centre of the goal",
                    "12": "Top left corner",
                    "13": "Top right corner"
                }
                goal_placement = goal_placement_dict[row[14]]

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

                goal_following_dict = {
                    "NA": "",
                    "1": "Open play",
                    "2": "Set piece",
                    "3": "Corner",
                    "4": "Free kick"
                }
                goal_following = goal_following_dict[row[20]]

                foot_dict = {
                    "NA": "",
                    "1": "right foot",
                    "2": "left foot",
                    "3": "head"
                }
                foot = foot_dict[row[18]]

                pattern = r"Goal!\s+(?P<home_team>[\w\s]+)\s+(?P<home_score>\d+),\s+(?P<away_team>[\w\s]+)\s+(?P<away_score>\d+)."

                
                match = re.search(pattern, row[4])

                if match:
                    home_team = match.group("home_team").strip()
                    away_team = match.group("away_team").strip()
                    home_score = int(match.group("home_score"))
                    away_score = int(match.group("away_score"))
                
                event_dict = {
                "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Home Team: {home_team}. ### Away Team: {away_team}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assist by: {assist}. ### Assist method: {assist_method}. ### Pitch Position: {pitch_position}. ### Goal Placement: {goal_placement}. ### Goal Following: {goal_following}. ### Foot: {foot}. ### Score: {home_team} {home_score}, {away_team} {away_score}. ### Assistant: {row[4]}"
                }

                event_dict["text"] += correct_player_names(row[4], player, assist)
                event_dict["text"] = event_dict["text"].replace("Goal!        Goal!", "Goal!")

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:

    reader_obj = csv.reader(file_obj)
    bbc_goals_total = 0

    with open('dataset_goals.jsonl', 'a') as f:
        for row in reader_obj:
        
            if row[14] == "Goal":
                event = row[14]
                time = row[6]
                event_team = row[15]
                opponent_team = row[16]
                player = row[17]
                assister = ""
                assist_method = row[22]
                pitch_position = row[19]
                goal_placement = row[20]
                goal_following = row[21]
                foot = row[24]

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
                    goal_following = row[21]
                elif "set piece" in row[12]:
                    goal_following = "Set Piece"
                else:
                    goal_following = row[23]

                # Regex to extract the home and away team scores
                pattern = r"Goal!\s+(?P<home_team>[\w\s]+)\s+(?P<home_score>\d+),\s+(?P<away_team>[\w\s]+)\s+(?P<away_score>\d+)."
                match = re.search(pattern, row[12])

                if match:
                    home_team = match.group("home_team").strip()
                    away_team = match.group("away_team").strip()
                    home_score = int(match.group("home_score"))
                    away_score = int(match.group("away_score"))
                
                event_dict = {
                "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Home Team: {home_team}. ### Away Team: {away_team}. ### Event Team: {row[15]}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assist by: {assister}. ### Assist Method: {assist_method}. ### Pitch Position: {pitch_position}. ### Goal Placement: {goal_placement}. ### Goal Following: {goal_following}. ### Foot: {foot}. ### Score: {home_team} {home_score}, {away_team} {away_score}. ### Assistant: {row[4]}"
                }

                # Replace players names to fix encoding issues
                event_dict["text"] += correct_player_names(row[12], row[17], assist)
                event_dict["text"] = event_dict["text"].replace("Goal!        Goal!", "Goal!")

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')