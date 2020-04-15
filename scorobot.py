from platforms.discordbot import DiscordBot
from dotenv import load_dotenv
import os
from games.game import Game, Tournament
from games.players import Team, SinglePlayer

if __name__ == '__main__':
    myBot = DiscordBot()
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    myBot.run(TOKEN)
    