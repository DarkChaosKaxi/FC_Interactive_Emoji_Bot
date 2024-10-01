from typing import Final
import os
import discord
from discord import app_commands
import random
import asyncio
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from emojis import get_emojis
from admins import check_admin
from players import scoreboard_reader
from players import save_player_list
from players import add_point
from players import get_show_player_list

# STEP 0: Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: Bot Setup
intents: Intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)

### Holiday Emoji Handler
async def emotional(message:Message) -> str:
    print('Getting emotional...')
    
    odds: float = float(0.1)                            # Defined game odds.
    rng: float = random.random()                        # RNG.

    #if random.random < odds:
    try:
        if odds > rng:
            holiday_emojis = get_emojis()               # Get emojis from emojis.py file.
            emoji:str = random.choice(holiday_emojis)   # RNG from emoji list.
            print(f'Emoji chosen: {emoji}')
            await message.add_reaction(emoji)           # Add RNG'd emoji.
            return emoji                                # Function returns emoji used.
        else:
            print('Game not running.')
    except Exception as e:
        print(e)
    return ''                                           # If failed, blank return.

### Clear reaction
async def clear_reaction(message:Message, emoji, user) -> None:
    print('Clearing reaction...')
    try:
        await message.remove_reaction(emoji, user)  # Remove reaction command.
    except Exception as e:
        print(e)
    return

### Clear bot reaction
async def clear_bot_reaction(message:Message, emoji) -> None:
    print('Clearing bot reaction...')
    await clear_reaction(message, emoji, client.user)   # Bot-specific to generic remove reaction.
    return

### Reaction Acknowledgment
@client.event
async def on_reaction_add(reaction, user) -> None:
    print(f'Reaction was added: {reaction} by {user}.') # Just a record for now, could be useful later.
    #print(f'Checking for {reaction}...')
    return

#Close command
def shutdown(author) -> None:
    try:
        if check_admin(author.id):                              # Checking with admins.py, handler for admin_ids.
            print("Shutting down bot!")
            save_player_list()                                  # Saving active memory.
            exit()
        else:
            print(f'{author} just tried to shutdown the bot!')  # Log back kill commands.
            #exit()
    except Exception as e:
        print('Failed exit.')
        print(e)
        #exit()
    return

#STEP 2: Message Response Functionality
async def message_reaction(message: Message, user_message: str) -> None:
    print(user_message)
    if not user_message:                            # Catch for non-matching messages. 
        print('!! Message was empty. !!')
        return
    if is_private := user_message[0] == '?':        # Catch for public v private.
        user_message = user_message[1:]
    if user_message == 'kill':                      # Stupid kill command.
        print('Attempting to leave...')
        shutdown(message.author)
        return
    elif user_message == 'show':
        try:
            if check_admin:
                print('Showing scoreboard...')
                response: str = await get_show_player_list(client)
                await message.author.send(response) if is_private else await message.channel.send(response)
            else:
                print('Non Admin tried to show scoreboard!')
        except Exception as e:
            print('Show failed.')
            print (e)
    elif user_message == 'smile':                   # Smile adds a heart and a little response.
        print('Smiling!')
        try:
            await message.add_reaction('🤍')
            message.author.send()
            response: str = 'Smile!'
            await message.author.send(response) if is_private else await message.channel.send(response)
            return
        except Exception as e:
            print(e)
    else:                                           # General handler for the emotional RNG nonsense.
        try:
            response: str = get_response(user_message)
            if response == '' or response == None:
                print('Response was empty.')
            else:
                print(f'Attempting to send response: {response}...')
                await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
            print(e)
        emo: str = ''
        
        try:
            emo = await emotional(message)          # RNG game startup.
        except Exception as e:
            print(e)
            return                                  # Fire escape.
        

        if emo != '':
            def check(reaction, user) -> bool:      # Checker function: return True if the emoji is same and user isn't bot.
                print(f'Checker found {reaction} from {user}!')
                print(f'Comparing {emo} and {reaction}... {(reaction == emo)}')
                return f'{reaction}' == emo and user.id != client.user.id
            
                ### Depricated code start...    ###
                for react in message.reactions:
                    if(react.emoji == emo and user != client.user):
                        print(f'Checker found reaction by {user}.')
                        return True

#                    print(f'Checking for emoji {react}...')
#                    user_list = [react.users()]
#                    for indi_user in user_list:
#                        print(f'Checking on {react} by {indi_user.name}...')
#                        if (react.emoji == emo and indi_user != client.user):
#                            print(f'Checker found something: {react.emoji} from {indi_user.name}.')
#                            return True
                print(f'Checker internal failure for {emo}.')
                return False
                ### ...Depricated code end.     ###

            try:
                print(f'Attempting reaction check for {emo}...')
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)   # 10-second timeout on emoji game.
                print(f'Reaction confirmation {reaction} by {user}.')
            except asyncio.TimeoutError:                                                            # If timeout, game ends with a sad message.
                print('Reaction check failed.')
                await message.reply(f'Aw... no one noticed the {emo}...',mention_author=False)      # Reply without mentions to show which message it was on.
            else:
                await clear_bot_reaction(message, emo)                                              # Clear bot reaction command on game success.
                print('Reaction check succeeded!.')
                add_point(user.id, reaction)                                                        # Add point to active memory scoreboard.
                await message.reply(f'{user} scored a point for {reaction}!',mention_author=False)  # Reply without mentions to show which message it was on.
        else:
            print('Didn\'t send emoji.')                                                          # Catch if an emoji wasn't sent (library empty).
        print('Done.')
        return


"""
async def on_reaction_add(message: Message) -> None:
    if message.author == client.user:
        print('Client user blah.')
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
"""

#STEP 3: Handling startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running.')             # Power-on print.
    scoreboard_reader()
    return

#STEP 4: Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:                   # Don't play with itself.
        return
    
    username: str = str(message.author)                 # Cast author to string.
    user_message: str = message.content                 # Message string.
    channel: str = str(message.channel)                 # Message channel.

    print(f'[{channel}] {username}: "{user_message}"')  # Log for messages.
    await message_reaction(message, user_message)       # Check message to see how to respond.
    return

#STEP 5: Main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()