from platforms.discordbot import DiscordBot
from dotenv import load_dotenv
import os
from games.game import Game, Tournament
from games.players import Team, SinglePlayer
from games.rules import SoccerChampionship
from globalcfg import backend

if __name__ == '__main__':
    
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    rules = SoccerChampionship("any")
    myTournament = Tournament("PES ELO", 1, rules)
    myBot = DiscordBot(myTournament)
    myBot.run(TOKEN)
    
    
