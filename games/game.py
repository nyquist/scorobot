import time
import random
from globalcfg import backend
from games.players import Team, SinglePlayer
from games.rules import SoccerChampionship

class Game:
    def __init__(self, team1, team2, score1, score2,duration='90'):
        global backend
        self.teams = (team1, team2)
        self.score = (score1, score2)
        self.date = time.time()
        self.duration = duration #90,120,11


class Tournament:
    
    def __init__(self, name, host_id, rules):
        global backend
        self.teams = set()
        self.games = []
        self.id = backend.addTournament(name, host_id)
        self.rules = rules
    def addGame(self, teamA, teamB, scoreA, scoreB):
        new_game = Game(Team(teamA,1), Team(teamB,1), scoreA, scoreB)
        return self.addGameObj(new_game)
    def addGameObj(self, game):
        self.games.append(game)
        self.teams.add(game.teams[0])
        self.teams.add(game.teams[1])
        game_details = (game.date, str(game.teams[0]), str(game.teams[1]), int(game.score[0]), int(game.score[1]), str(game.duration), self.id)
        return backend.addGame(game_details)
    def getGames(self, last_hours = 0):
        return backend.getGames(self.id, last_hours, teams_filter = [])
    def getTeams(self):
        return [row[0] for row in backend.getTeams(self.id)]

    def getRanking(self, last_hours = 0, teams_filter=[]):
        teams = dict()
        for game in backend.getGames(self.id, last_hours, teams_filter):
            teamA = game[2]
            teamB = game[3]
            if teamA in teams:
                old_totals = teams[teamA]
            else:
                old_totals = None
            teams[teamA] = self._teamTotals(old_totals, game[4], game[5])
            if teamB in teams:
                old_totals = teams[teamB]
            else:
                old_totals = None
            teams[teamB] = self._teamTotals(old_totals, game[5], game[4])
        return sorted(teams.items(), key= self.rules.rank, reverse=True)
    
    def _teamTotals(self, old_totals, gf, ga):
        if old_totals is None:
            totals = {
                'w':1 if gf>ga else 0,
                'd':1 if gf==ga else 0,
                'l':1 if gf<ga else 0,
                'gf':gf, 
                'ga':ga, 
                'p':self.rules.getPoints(gf,ga)
            }
        else:
            totals = {
                'gf': old_totals['gf'] + gf,
                'ga': old_totals['ga'] + ga,
                'w': old_totals['w'] + 1 if gf>ga else old_totals['w'],
                'l': old_totals['l'] + 1 if gf<ga else old_totals['l'],
                'd': old_totals['d'] + 1 if gf==ga else old_totals['d'],
                'p': old_totals['p'] + self.rules.getPoints(gf,ga)
            }
        return totals
        
    
        
if __name__ == "__main__":
    team_names = ["A","B","C","D","E","F","G","H"]
    team1 = random.choice(team_names)
    team_names.remove(team1)
    team2 = random.choice(team_names)
    rules = SoccerChampionship('any')
    new_tournament = Tournament('Champions League 2020','Discord#Fotbal', rules)
    new_game = Game(Team(team1,1), Team(team2,1), int(random.randint(0,4)), int(random.randint(0,4)))
    new_tournament.addGameObj(new_game)
    new_tournament.getRanking()
    for line in new_tournament.getRanking():
        print ("{T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3}".format(T=line[0],M=line[1]['w']+line[1]['d']+line[1]['l'], W=line[1]['w'], D=line[1]['d'], L=line[1]['l'], GF=line[1]['gf'], GA=line[1]['ga'], P=line[1]['p']))