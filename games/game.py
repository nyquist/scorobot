import datetime
import time
import sqlite3
import random
from players import Team, SinglePlayer

class Game:
    def __init__(self, team1, team2, score1, score2,duration='90'):
        self.teams = (team1, team2)
        self.score = (score1, score2)
        self.date = time.time()
        self.duration = duration #90,120,11


class Championship:
    def __init__(self, venue, venue_id, championship_name):
        self.teams = set()
        self.games = []
        db_file = "games.db"
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self._setupDB()
        self.championship_id = self._addChampionshiptoDB(venue, venue_id, championship_name)
    
    def _setupDB(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, date TEXT NOT NULL, team1 TEXT NOT NULL, team2 TEXT NOT NULL, scor1 INT NOT NULL, scor2 INT NOT NULL, duration TEXT NOT NULL, championship_id INT NOT NULL)')
        self.c.execute('CREATE TABLE IF NOT EXISTS championships(id INTEGER PRIMARY KEY, name TEXT NOT NULL, venue TEXT NOT NULL, venue_id TEXT NOT NULL, UNIQUE(name, venue, venue_id))')
        # self.c.execute('SLECT rowid FROM championships WHERE ')
    def _addChampionshiptoDB(self, venue, venue_id, championship_name):
        try:
            self.c.execute('INSERT INTO championships (name, venue, venue_id) VALUES (?,?,?)',(championship_name, venue, venue_id))
            self.conn.commit()
            return self.c.lastrowid
        except sqlite3.IntegrityError as e:
            self.c.execute('SELECT rowid FROM championships WHERE name=? AND venue = ? AND venue_id = ?',(championship_name, venue, venue_id))
            result = self.c.fetchone()
            return result[0]
    
    def addGame(self, game):
        self.games.append(game)
        self.teams.add(game.teams[0])
        self.teams.add(game.teams[1])
        game_details = (str(game.date), str(game.teams[0]), str(game.teams[1]), int(game.score[0]), int(game.score[1]), str(game.duration), self.championship_id)
        return self._addGameToDB(game_details)
        
    
    def _addGameToDB(self, game_details):
        self.c.execute('INSERT INTO games (date, team1, team2, scor1, scor2, duration, championship_id) VALUES(?,?,?,?,?,?,?)',game_details)
        self.conn.commit()
        return self.c.lastrowid
        
    def listGames(self):
        self.c.execute('SELECT * FROM games WHERE championship_id = ?',(self.championship_id,))
        return self.c.fetchall()
    def getRanking(self):
        teams = dict()
        for game in self.listGames():
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
        return sorted(teams.items(), key= self._getRankingValue, reverse=True)
    def _teamTotals(self, old_totals, gf, ga):
        if old_totals is None:
            totals = {
                'w':1 if gf>ga else 0,
                'd':1 if gf==ga else 0,
                'l':1 if gf<ga else 0,
                'gf':gf, 
                'ga':ga, 
            }
        else:
            totals = {
                'gf': old_totals['gf'] + gf,
                'ga': old_totals['ga'] + ga,
                'w': old_totals['w'] + 1 if gf>ga else old_totals['w'],
                'l': old_totals['l'] + 1 if gf<ga else old_totals['l'],
                'd': old_totals['d'] + 1 if gf==ga else old_totals['d']
            }
        return totals
        
    def _getRankingValue(self,item):
        key = item[0]
        w = item[1]['w']
        d = item[1]['d']
        l = item[1]['l']
        gf = item[1]['gf']
        ga = item[1]['ga']
        vp = 3
        dp = 1
        lp = 0
        return w*vp + d*dp + l*lp
        
if __name__ == "__main__":
    team_names = ["A","B","C","D","E","F","G","H"]
    team1 = random.choice(team_names)
    team_names.remove(team1)
    team2 = random.choice(team_names)
        
    new_game = Game(Team(team1,1), Team(team2,1), int(random.randint(0,4)), int(random.randint(0,4)))
    new_championship = Championship('Discord','discord_id','Champions League 2')
    new_championship.addGame(new_game)
    new_championship.getRanking()
    for value in new_championship.getRanking():
        print (value)