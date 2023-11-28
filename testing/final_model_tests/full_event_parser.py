import csv
import json
import re

# Dictionaries

assist_method_dict = {
    "0": "",
    "1": "Pass",
    "2": "Cross",
    "3": "Headed pass",
    "4": "Through ball"
}

shot_placement_dict = {
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

shot_following_dict = {
    "NA": "",
    "1": "Open play",
    "2": "Set piece",
    "3": "Corner",
    "4": "Free kick"
}


foot_dict = {
    "NA": "",
    "1": "right foot",
    "2": "left foot",
    "3": "head"
}

shot_outcome_dict = {
    "NA": "",
    "1": "Saved",
    "2": "Missed",
    "3": "Blocked",
    "4": "Hit the bar"
}

with open('liverpool_v_norwich.csv', 'r', encoding='utf-8') as file_obj:
    
    reader_obj = csv.reader(file_obj)

    with open('full_match_dataset.jsonl', 'w') as f:
        for row in reader_obj:
            
            ###### ATTEMPTS ######

            if row[5] == "1" and row[16] == "0":
                event = "Attempt"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                assister = ""
                if row[11] != "NA":
                    assister = row[11]
                attempt_result = ""

                # Dictionary Lookups
                assist_method = assist_method_dict[row[19]]
                attempt_placement = shot_placement_dict[row[14]]
                pitch_position = pitch_position_dict[row[17]]
                attempt_following = shot_following_dict[row[20]]
                foot = foot_dict[row[18]]
                attempt_result = shot_outcome_dict[row[15]]

                # Attempt result conditionals
                if "hits the right post" in row[4]:
                    attempt_placement = "Hits the right post"
                elif "hits the left post" in row[4]:
                    attempt_placement = "Hits the left post"

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assister: {assister}. ### Assist Method: {assist_method}. ### Attempt Result: {attempt_result}. ### Foot: {foot}. ### Pitch Position: {pitch_position}. ### Attempt Placement: {attempt_placement}. ### Attempt Following: {attempt_following}. ### Assistant: {row[4]}"
                }

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

            ###### GOALS ######

            if row[16] == "1":
                event = "Goal"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                assist = ""
                if row[11] != "NA":
                    assist = row[11]

                # Dictionary Lookups
                assist_method = assist_method_dict[row[19]]
                goal_placement = shot_placement_dict[row[14]]
                pitch_position = pitch_position_dict[row[17]]
                goal_following = shot_following_dict[row[20]]
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

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

            ###### SUBS ######

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
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player On: {player_on}. ### Player Off: {player_off}. ### Reason: {reason}. ### Assistant: {row[4]}"
                }

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

            ###### OFFSIDES ######

            if row[5] == "9":
                event = "Offside"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                passer = row[11]
                offside_player = row[10]

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Passer: {passer}. ### Offside Player: {offside_player}. ### Assistant: {row[4]}"
                }

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

            ###### CARDS ######

            if row[5] == "4" or row[5] == "5" or row[5] == "6":
                event = "Card"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                reason = ""
                player_dismissed = ""
                comment = ""

                card_dict = {
                    "4": "First yellow card",
                    "5": "Second yellow card",
                    "6": "Red card"
                }
                card_type = card_dict[row[5]]

                if "for" in row[4]:
                    parts = row[4].split("for", 1)
                    reason = parts[1].strip()
                    reason = reason.rstrip('.')

                if row[5] == "4":
                    player_dismissed = "No"
                    comment = "Booking"
                else:
                    player_dismissed = "Yes"
                    comment = "Dismissal"

                # fixes errors in the dataset
                if "Second yellow" in row[4]:
                    card_type = card_dict["5"]
                    player_dismissed = "Yes"
                    comment = "Dismissal"

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Card type: {card_type}. ### Reason: {reason}. ### Player dismissed?: {player_dismissed}. ### Assistant: {row[4]}"
                }

                # Add the dictionary to the list
                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

            ###### CORNERS ######

            if row[5] == "2":
                event = "Corner"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                conceded_by = row[10]

                if conceded_by == "NA":
                   continue

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Conceded by: {conceded_by}. ### Assistant: {row[4]}"
                }

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

            ###### FOULS ######

            if row[5] == "3":
                event = "Foul"
                time = row[3]
                event_team = row[8]
                opponent_team = row[9]
                player = row[10]
                
                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assistant: {row[4]}"
                }

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')
            

