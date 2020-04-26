class GameRules:
    def __init__(self):
        return
    def getPoints(self):
        return 0
    def getElo(self):
        return 0
        
class Championship(GameRules):
    # Each team plays any other team
    def __init__(self, home_away, vp, dp, lp=0, lb =0, wb = 0, lb_diff=None, wb_diff=None):
        self.vp = vp
        self.dp = dp
        self.lp = lp
        self.wb = wb
        self.lb = lb
        self.lb_diff = lb_diff
        self.wb_diff = wb_diff
        GameRules.__init__(self)
        
    def getPoints(self, my_score, opponent_score):
        if my_score == opponent_score:
            return self.dp
        else:
            winner = self.vp
            loser = self.lp
            if self.wb_diff is not None and abs(my_score-opponent_score) > self.wb_diff:
                winner = winner + self.wb
            if self.lb_diff is not None and abs(my_score-opponent_score) < self.lb_diff:
                loser = loser + self.lb
            if my_score > opponent_score:
                return winner
            else:
                return loser
    
    def rank(self,item):
        ## TO move into rules
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

class SoccerChampionship(Championship):
    def __init__(self, home_away):
        Championship.__init__(self, home_away,3,1)

class HandballChampionship(Championship):
    def __init__(self, home_away):
        Championship.__init__(self, home_away,2,1)

class RugbyChampionship(Championship):
    def __init__(self, home_away):
        Championship.__init__(self, home_away,4, 2,lp =0, wb=7, lb=7)


class Cup(GameRules):
    # Bracket elimination system
    def __init__(self):
        GameRules.__init__(self)

class WorldCup(Championship, Cup):
    # Groups followed by Cup system
    def __init__(self):
        GameRules.__init__(self)

class ELOCup(Championship):
    #Random games. Only the ELO counts
    def __init__(self):
        GameRules.__init__(self)
