from langchain import PromptTemplate
from langchain import HuggingFacePipeline
from language_model import llm

import streamlit as st
import torch
import transformers

# to run the app enter the following in the commandline:
# python3 -m streamlit run streamlit_MascotAI.py

# TO DO
#
# 2. Find a suitable api (harder than it seemed)
# 3. Build the backend for the API

st.set_page_config(page_title = "Mascot AI", page_icon = ":robot:")
st.header("Mascot AI")

event_dropdown = st.selectbox(
    "Choose an event:",
    ("", "Goal", "Attempt", "Substitution", "Offside", "Card", "Corner", "Foul")
)

event_team = ""
opponent_team = ""

if event_dropdown != "":

    event_team_col, opponent_team_col = st.columns(2)
    with event_team_col:
        event_team = st.text_input("Event Team:")
    with opponent_team_col:
        opponent_team = st.text_input("Opponent Team:")

#######################################
#                                     #
#~~~~~~~~~~~~~~  GOALS  ~~~~~~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Goal":

    home_team_choice = st.radio("Who is the home team?", ["Event Team", "Opponent Team"])

    if home_team_choice == "Event Team":
        home_team = event_team
        away_team = opponent_team
    else:
        home_team = opponent_team
        away_team = event_team

    player_col, card_type_col = st.columns(2)
    with player_col:
        player = st.text_input("Player ")
    with card_type_col:    
        assist = st.text_input("Assister (if applicable) ")

    assist_method_col, pitch_position_col = st.columns(2)
    with assist_method_col:
        assist_method = st.selectbox(
            "Assist method (if applicable):",
            ("", "Pass", "Cross", "Headed pass", "Through ball")
        )
    with pitch_position_col:
        pitch_position = st.selectbox(
            "Pitch position: ",
            ("", "Attacking half", "Defensive half", "Centre of the box", "Left wing", "Right wing", "Difficult angle and long range", "Difficult angle on the left", "Difficult angle on the right", "Left side of the box", "Left side of the six yard box", "Right side of the box", "Right side of the six yard box", "Very close range", "Penalty spot", "Outside the box", "Long range", "More than 35 yards", "More than 40 yards")
        )

    goal_placment_col, attempt_following_col = st.columns(2)
    with goal_placment_col:
        goal_placement = st.selectbox(
            "Goal Placement: ",
            ("", "Bottom left corner", "Bottom right corner", "Centre of the goal", "Top centre of the goal", "Top left corner", "Top right corner")
        )
    with attempt_following_col:
        goal_following = st.selectbox(
            "Goal Following: ",
            ("", "Open play", "Set piece", "Corner", "Free kick")
        )

    foot = st.selectbox(
        "Foot: ",
        ("Left foot", "Right foot", "Head")
    )

    home_team_score_col, away_team_score_col = st.columns(2)
    with home_team_score_col:
        home_team_score = st.number_input("Home Team Score:", min_value=0, max_value=20, value=1, step=1)
    with away_team_score_col:
        away_team_score = st.number_input("Away Team Score:", min_value=0, max_value=20, value=1, step=1)

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Home Team: {home_team}. ### Away Team: {away_team}. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assist by: {assist}. ### Assist method: {assist_method}. ###  Pitch Position: {pitch_position}. ### Goal Placement: {goal_placement}. ### Goal Following: {goal_following}. ### Foot: {foot}. ### Score: {home_team} {home_team_score}, {away_team} {away_team_score}. ### Assistant: Goal!"""

            result = llm(prompt)

# Model is inconsistent with including the word "Goal" or not
            if "Goal!" in result:
                st.write("\U000026BD " + result)
            else:
                st.write("\U000026BD Goal!" + result)


#######################################
#                                     #
#~~~~~~~~~~~~  ATTEMPTS   ~~~~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Attempt":

    player_col, card_type_col = st.columns(2)
    with player_col:
        player = st.text_input("Player ")
    with card_type_col:    
        assist = st.text_input("Assister (if applicable) ")

    attempt_result_col, pitch_position_col = st.columns(2)
    with attempt_result_col:
        attempt_result = st.selectbox(
            "Attempt Result:",
            ("", "Saved", "Missed", "Blocked", "Hit the bar")
        )
    with pitch_position_col:
        pitch_position = st.selectbox(
            "Pitch position: ",
            ("", "Attacking half", "Defensive half", "Centre of the box", "Left wing", "Right wing", "Difficult angle and long range", "Difficult angle on the left", "Difficult angle on the right", "Left side of the box", "Left side of the six yard box", "Right side of the box", "Right side of the six yard box", "Very close range", "Penalty spot", "Outside the box", "Long range", "More than 35 yards", "More than 40 yards")
        )

    attempt_placment_col, attempt_following_col = st.columns(2)
    with attempt_placment_col:
        attempt_placement = st.selectbox(
            "Attempt Placement: ",
            ("", "Bit too high", "Too High", "Hide and wide", "Blocked", "Hits the bar", "Misses to the left", "Misses to the right", "Bottom left corner", "Bottom right corner", "Centre of the goal", "Top centre of the goal", "Top left corner", "Top right corner")
        )
    with attempt_following_col:
        attempt_following = st.selectbox(
            "Attempt Following: ",
            ("", "Open play", "Set piece", "Corner", "Free kick")
        )

    foot = st.selectbox(
        "Foot: ",
        ("Left foot", "Right foot", "Head")
    )

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assist: {assist}. ### Attempt Result: {attempt_result}. ### Foot: {foot} ### Pitch Position: {pitch_position}. ### Attempt Placement: {attempt_placement}. ### Attempt Following: {attempt_following }. ### Assistant: Attempt"""

            result = llm(prompt)
            st.write("\U0001F945 Attempt" + result)

#######################################
#                                     #
#~~~~~~~~~~  SUBSTITUTIONS   ~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Substitution":

    player_col, card_type_col = st.columns(2)
    with player_col:
        player_on = st.text_input("Player going on: ")
    with card_type_col:    
        player_off = st.text_input("Player coming off: ")

    reason = st.selectbox(
        "Reason: ",
        ("None", "Injury")
        )

    if reason == "None":
        reason = ""

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player On: {player_on}. ### Player Off: {player_off}. ### Reason: {reason}. ### Assistant: Substitution"""

            result = llm(prompt)
            st.write("\U0001F504 Substitution" + result)

#######################################
#                                     #
#~~~~~~~~~~~~~  OFFSIDES  ~~~~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Offside":

    player_col, card_type_col = st.columns(2)
    with player_col:
        passer = st.text_input("Passer: ")
    with card_type_col:    
        offside_player = st.text_input("Offside Player: ")

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Passer: {passer}. ### Offside Player: {offside_player}. ### Assistant: Offside"""

            result = llm(prompt)
            st.write("\U0001F3C3 Offside" + result)

#######################################
#                                     #
#~~~~~~~~~~~~~~~  CARDS  ~~~~~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Card":

    player_col, card_type_col = st.columns(2)
    with player_col:
        player = st.text_input("Player: ")
    with card_type_col:    
        card_type= st.selectbox(
            "Card: ",
            ("", "First yellow card", "Second yellow card", "Red card"))

    if card_type == "First yellow card":
        player_dismissed = "No"
    else:
        player_dismissed = "Yes"
    
    reason = st.selectbox(
        "Reason: ",
        ("", "A bad foul", "Hand ball", "Violent conduct", "Dangerous play", "Excessive Celebration", "Time wasting", "Diving", "Cynical foul", "Unsportsmanlike behaviour")
    )

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Card type: {card_type}. ### Reason: {reason} ### Player dismissed?: {player_dismissed}. ### Assistant: {player}"""

            result = llm(prompt)

            if card_type == "Red card":
                st.write("\U0001F7E5 " + player + " " + result)
            if card_type == "Second yellow card":
                st.write("\U0001F7E8 \U0001F7E8 " + player + " " + result)
            else:
                st.write("\U0001F7E8 " + player + " " + result)

#######################################
#                                     #
#~~~~~~~~~~~~~~  CORNERS  ~~~~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Corner":

    conceded_by = st.text_input("Conceded by: ")

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Conceded by: {conceded_by}. ### Assistant: Corner"""

            result = llm(prompt)
            st.write("\U0001F6A9 Corner" + result)

#######################################
#                                     #
#~~~~~~~~~~~~~~  FOULS  ~~~~~~~~~~~~~~#
#                                     #
#######################################

if event_dropdown == "Foul":

    player = st.text_input("Player: ")

    if st.button("Submit"):
        with st.spinner("Processing..."):
            prompt = f"""text: ### Human: Below is a series of pieces of information describing an event in a soccer match paired with an output that describes the event based on the pieces of information. Acting as an expert soccer commentator, describe this event in an informative and engaging manner. ### Event: {event_dropdown}. ### Time: 5. ### Event Team: {event_team}. ### Opponent Team: {opponent_team}. ### Player: {player}. ### Assistant: Foul"""

            result = llm(prompt)
            st.write("\U0001F4E3 Foul" + result)