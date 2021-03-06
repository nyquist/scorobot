import globalcfg
from platforms.discordbot import DiscordBot
from games.game import Game, Tournament
from games.players import Team, SinglePlayer
from games.rules import SoccerChampionship


if __name__ == '__main__':
    rules = SoccerChampionship("any")
    myTournament = Tournament("PES ELO", 1, rules)
    myBot = DiscordBot(tournament=myTournament, testing=globalcfg.TESTING)
    myBot.run(globalcfg.TOKEN)
    
