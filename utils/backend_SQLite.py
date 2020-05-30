import sqlite3
from utils.backend import Backend
from datetime import timedelta
import time

class SQLiteDB(Backend):
    def __init__(self,db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        Backend.__init__(self)
        
        
    def setup(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, date TEXT NOT NULL, team1 TEXT NOT NULL, team2 TEXT NOT NULL, scor1 INT NOT NULL, scor2 INT NOT NULL, duration TEXT NOT NULL, championship_id INT NOT NULL)')
        self.c.execute('CREATE TABLE IF NOT EXISTS championships(id INTEGER PRIMARY KEY, name TEXT NOT NULL, host_id TEXT NOT NULL, UNIQUE(name, host_id))')
        
    def addTournament(self, name, host_id):
        try:
            self.c.execute('INSERT INTO championships (name, host_id) VALUES (?,?)',(name, host_id))
            self.conn.commit()
            return self.c.lastrowid
        except sqlite3.IntegrityError:
            self.c.execute('SELECT rowid FROM championships WHERE name=? AND host_id = ?',(name, host_id))
            result = self.c.fetchone()
            return result[0]
            
    def addGame(self, game_details):
        self.c.execute('INSERT INTO games (date, team1, team2, scor1, scor2, duration, championship_id) VALUES(?,?,?,?,?,?,?)',game_details)
        self.conn.commit()
        print(game_details)
        return self.c.lastrowid
        
    def getGames(self, championship_id, last_hours):
        if last_hours > 0:
            self.c.execute('SELECT * FROM games WHERE championship_id = ? AND date >= ?',(championship_id,time.time() - 60*60*last_hours))
        else:
            self.c.execute('SELECT * FROM games WHERE championship_id = ?',(championship_id,))
        return self.c.fetchall()
    
    def getTeams(self, championship_id):
        self.c.execute('SELECT DISTINCT team1 FROM games UNION SELECT DISTINCT team2 FROM games')
        return self.c.fetchall()

#if __name__ == '__main__':
    
    