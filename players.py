from typing import Final
import os
import discord
from discord import Intents, Client, Message
from emojis import get_emoji_scores
from emojis import get_emojis

# user_id, emoji, count
blank_player: Final[str] = ['0','🛑','0']

player_list = [blank_player]

def initialize_player_list():
    player_list = [blank_player]
    return

### Get Player List in Active Memory
def get_player_list():
    return player_list

def get_text_player_list(temp_player_list) -> str:
    print('Preparing raw text...')
    raw_text: str = ''
    startchecker: bool = True
    for player in temp_player_list:
        if player[0] == blank_player[0] and player[1] == blank_player[1]:
            print('Not adding blank player...')
        else:
            if not startchecker:
                raw_text += '\n'
            else:
                startchecker = False
            player_text: str = f'{player[0]} {player[1]} {player[2]}'
            print(f'Adding {player_text} to raw.')
            raw_text += player_text
    print('Raw text obtained.')
    return raw_text

async def get_show_player_list(client) -> str:
    print('Gathering replacement show player data...')
    try:
        print(player_list)
        show_player_list = []
        for player in player_list:
            if player[0] != blank_player[0]:
                print(f'Fetching user info for {player[0]}...')
                user = await client.fetch_user(int(player[0]))
                show_player_list.append([user.name,player[1],player[2]])
            else:
                print('Bad user call.')
        
        print(show_player_list)
        return get_text_player_list(show_player_list)
    except Exception as e:
        print('Failed gather.')
        print(e)
        return 'Sorry... list failure.'

### Add Player to Existing Active Memory
def add_player(player_id: int, emoji: str, count: int = 1) -> None:
    print(f'Adding player {player_id} with {emoji} scoring {count}...')
    try:
        player_list.append([f'{player_id}',f'{emoji}',f'{count}'])
        print('Player list append success.')
    except Exception as e:
        print(e)
        print('Player list append failure.')
    return

### Load Player List to Active Memory
def load_player_list(file_data) -> None:
    print('Attempting to load player list...')
    # replacing end splitting the text
    # when newline ('\n') is seen.
    #data_into_list = data.split("\n")
    #print(data_into_list)
    #initialize_player_list()
    list_data = file_data.split('\n')
    for player in list_data:
        player_data = player.split(' ')
        print(f'Adding player {player_data} to list...')
        add_player(player_data[0], player_data[1], count=player_data[2])
    print(player_list)
    return
    print('Data split. Attempting to parse each row.')
    try:
        for row in list_data:
            player = row.split(' ')
            print(f'Broken attempt with {player[0]}...')
            add_player(player[0],player[1],count=player[2])
        print('Player list load success!')
    except Exception as e:
        print('Player list load fail.')
        print(e)
    return

### Get Score of Player/Emoji
def get_score(player_id: int, emoji: str) -> int:
    print(f'Looking for count of {player_id} with emoji {emoji}...')
    for player in player_list:
        if player[0] == f'{player_id}' and player[1] == emoji:
            print(f'Found player {player[0]} with emoji {player[1]}.')
            return player[3]
    return 0

def get_player_scores() -> str:
    
    for player in player_list:

        return
    return ''

### Add Point to Player/Emoji
def add_point(player_id: int, emoji: str) -> None:
    print(f'Attempting to add point to {player_id} for {emoji}...')
    for player in player_list:
        if player[0] == f'{player_id}' and player[1] == f'{emoji}':
            print(f'Found player {player[0]} with emoji {player[1]}.')
            try:
                score: int = int(player[2])
                score += 1
                player[2] = f'{score}'
                print(f'Updated score to {player[2]}.')
            except Exception as e:
                print(e)
            return
    print(f'Player {player_id} with {emoji} not found.')
    add_player(player_id, emoji)
    return

### File Reader Handler
def scoreboard_reader() -> None:
    """
    with open('scoreboard.txt', 'r') as f:
        scoreboard = int(f.readline())
    try:
        client.run(TOKEN)
    finally:
        with open('scoreboard.txt', 'w') as f:
            f.write(scoreboard)
    """

    try:
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "scoreboard.txt"
        abs_file_path = os.path.join(script_dir, rel_path)

        print('Attempting to open scoreboard...')
        scoreboard_file = open(abs_file_path, "r")      # File in read mode.
        print('Attempting to read scoreboard...')
        scoreboard_data = scoreboard_file.read()        # Data retreivable in str.
        print('Attempting to load player list from scoreboard...')
        print(scoreboard_data)
        load_player_list(scoreboard_data)               # Import players to active list.
        print('Closing scoreboard file...')
        scoreboard_file.close()                         # Close file.
    except Exception as e:
        print('Failed to open scoreboard.')
        print(e)
    return

def save_player_list() -> None:

    try:
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "scoreboard.txt"
        abs_file_path = os.path.join(script_dir, rel_path)

        print('Attempting to write scoreboard...')
        #scoreboard_file = open(abs_file_path, "w")   # File in read mode.
        
        try:
            with open(abs_file_path, 'w') as scoreboard_file:
                raw_text: str = get_text_player_list(player_list)
                print('Writing...')
                scoreboard_file.write(raw_text)
                print('Save succeeded!')
                print(raw_text)
        except Exception as e:
            print('Save failed.')
            print(e)

        scoreboard_file.close()                         # Close file.
    except Exception as e:
        print('Failed to open scoreboard.')
        print(e)

    return