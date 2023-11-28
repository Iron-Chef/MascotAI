import csv
import json
import sys
sys.path.append("..")
from character_rendering import correct_player_names

# Open file 
with open('../european_leagues.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    european_cards_total = 0
      
    # Iterate over each row in the csv 
    with open('./dataset_cards.jsonl', 'w') as f:
        for row in reader_obj:

            # Check for first yellow, second yellow, or red card event
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
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Card type: {card_type}. ### Reason: {reason}. ### Player dismissed?: {player_dismissed}. ### Assistant: {comment}. {row[4]}"
                }

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')

with open('../BBC_Commentary_Bigger.csv', 'r', encoding='utf-8') as file_obj:
      
    reader_obj = csv.reader(file_obj)
    bbc_cards_total = 0

    with open('./dataset_cards.jsonl', 'a') as f:
        for row in reader_obj:

            if row[14] == "Card":
                event = "Card"
                time = row[6]
                event_team = row[15]
                opponent_team = row[16]
                player = row[17]
                card_type = ""
                reason = row[26].replace("for ", "", 1).strip()
                player_dismissed = ""
                comment = ""

                if row[27] == "yellow":
                    card_type = "First yellow card"
                elif row[27] == "2nd Yellow":
                    card_type = "Second yellow card"
                elif row[27] == "red":
                    card_type = "Red card"

                if card_type == "Second yellow card" or card_type == "Red card":
                    player_dismissed = "Yes"
                    comment = "Dismissal"
                else:
                    player_dismissed = "No"
                    comment = "Booking"

                event_dict = {
                    "text": f"### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event}. ### Time: {time}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Card type: {card_type}. ### Reason: {reason}. ### Player dismissed?: {player_dismissed}. ### Assistant: {comment}. {row[12]}"
                }

                event_json = json.dumps(event_dict)
                f.write(event_json + '\n')