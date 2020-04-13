class Team:
    def __init__(self, team_name, max_size=100):
        self.team_name = team_name
        if max_size < 1:
            raise Exception('Invalid size :{}'.format(max_size))
        self.max_size = max_size
        self.players = set()
        
    def __str__(self):
        return self.team_name
        
    def addPlayer(self, player_name):
        if len(self.players) < self.max_size:
            self.players.add(player_name)
        else:
            raise Exception('Team is full! {} out of {} players'.format(self.max_size, self.max_size))
        
    def removePlayer(self, player_name):
        self.players.remove(player_name)
        
class SinglePlayer(Team):
    def __init__(self, player_name):
        Team.__init__(self, player_name, 1)
        self.players.add(player_name)
        
if __name__ == "__main__":
    test_team = Team("Test Team",2)
    test_player = SinglePlayer("P1")
    test_team.addPlayer("P2")
    test_team.addPlayer("P3")
    try:
        test_team.addPlayer("P4")
    except Exception as e:
        print ("Caught exception: " + str(e))
    try:
        test_player.addPlayer("P5")
    except Exception as e:
        print ("Caught exception: " + str(e))
    test_team.removePlayer("P3")
    test_team.addPlayer("P4")
    assert (test_team.players == {'P4', 'P2'}), "Error asserting team"
    assert (test_player.players == {'P1'}), "Error asserting player"