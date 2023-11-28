import re

# Regex functions to fit each type of event
# Replaces incorrectly encoded player names

def correct_player_names(text, player, assist):
    
    player_pattern = r"(\. )([^\(]+)\("
    correct_player_name = player.title()
    text = re.sub(player_pattern, r"\1" + correct_player_name + " (", text)

    if assist:
        assist_pattern = r"(Assisted by )([^with|following]+)( with| following|$)"
        correct_assist_name = assist.title()
        text = re.sub(assist_pattern, r"\1" + correct_assist_name + r"\3", text)

    return text

def correct_player_names_substitutions(text, player_on, player_off):
    
    on_pattern = r"(\.|\,)\s*([^\.\,]+?)\s*replaces"
    text = re.sub(on_pattern, r"\1 " + player_on.title() + " replaces", text)

    off_pattern = r"replaces\s*([^\.\,]+?)(\.|because)"
    text = re.sub(off_pattern, "replaces " + player_off.title() + " " + r"\2", text)

    text = re.sub(r"\s+\.", ".", text)
    text = re.sub(r"\.+", ".", text)
    
    return text

def correct_player_names_offsides(text, passer, offside_player):
    passer_pattern = r"(\. )([^\.]+)( tries)"
    correct_passer_name = passer.title()
    text = re.sub(passer_pattern, r"\1" + correct_passer_name + r"\3", text)

    offside_player_pattern = r"(but )([^\.]+)( is caught)"
    correct_offside_player_name = offside_player.title()
    text = re.sub(offside_player_pattern, r"\1" + correct_offside_player_name + r"\3", text)

    return text

def correct_player_names_fouls(text, player):

    pattern = r"(Foul by )([^(\(]+)"
    correct_name = player.title()
    text = re.sub(pattern, r"\1" + correct_name + " ", text)

    return text

def correct_player_names_corners(text, conceded_by):

    pattern = r"(Conceded by )([^\.]+)"
    correct_name = conceded_by.title()
    text = re.sub(pattern, r"\1" + correct_name, text)

    text = re.sub(r"(Corner,)\s{2}", r"\1 ", text)

    return text
