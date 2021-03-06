import re
import time
## This platform is used to get os number. It's not platforms
import platform
import subprocess
from fuzzywuzzy import fuzz


class Validator:
    def __init__(self, teamA, teamB, scoreA, scoreB, tournament):
        self.scoreA = scoreA
        self.scoreB = scoreB
        self.validated = False
        self.TTL = 3
        self.tournament = tournament
        self.gameId = None
        self.teamA, self.teamAisKnown = self.fuzzyName(teamA)
        self.teamB, self.teamBisKnown = self.fuzzyName(teamB)

    def fuzzyName(self, team):
        known_teams = self.tournament.getTeams()
        fuzzy_limit = 70
        if team in known_teams:
            return (team, "")
        else:
            fuzzyRatios = {teamName: fuzz.WRatio(team, teamName) for teamName in known_teams}
            fuzzyOptions = {key: item for key, item in fuzzyRatios.items() if item > fuzzy_limit}
            #print (team,fuzzyRatios)
            #print (team,fuzzyOptions)
            if 100 in fuzzyOptions.values():
                for key, value in fuzzyOptions.items():
                    if value == 100:
                        return (key, " [?100]")
            elif len(fuzzyOptions.keys()) == 1:
                return (list(fuzzyOptions.keys())[0], " [?{}]".format(list(fuzzyOptions.values())[0]))
            else:
                return (team, " [NEW]")

    def confirm(self):
        self.validated = True
        if self.tournament is not None:
            self.gameId = self.tournament.addGame(self.teamA, self.teamB, self.scoreA, self.scoreB)
            print("Adding game:", self.gameId, self)
            
        return self.gameId
    def __str__(self):
        return "{}-{} {}-{}.".format(self.teamA, self.teamB, self.scoreA, self.scoreB)    


class BotPlatform:
    def __init__(self, tournament = None, testing = False):
        self.tournament = tournament
        self.lastValid = None
        self.lastCancelled = None
        self.toBeConfirmed = None
        self.toReport = None
        self.testing = testing
        self.reactions = {
        'result': {
            'is': self._isResult,
            'do': lambda *a: '**{}**{}-**{}**{}: {} - {} ? Please confirm'.format(self.toBeConfirmed.teamA, self.toBeConfirmed.teamAisKnown,self.toBeConfirmed.teamB,self.toBeConfirmed.teamBisKnown, self.toBeConfirmed.scoreA, self.toBeConfirmed.scoreB)
            },
        'yes': {
            'is': lambda m: self.genericReaction(m, r"^(yes|y)$",r"^(ok)$"),
            'do': lambda *a: 'Added #{}: **{}**{}-**{}**{}: {}-{}'.format(self.lastValid.gameId, self.lastValid.teamA, self.lastValid.teamAisKnown, self.lastValid.teamB, self.lastValid.teamBisKnown, self.lastValid.scoreA, self.lastValid.scoreB, )
            },
        'no': {
            'is': lambda m: self.genericReaction(m, r"^(no?)$", r"^(cancel)$"),
            'do': lambda *a: 'Canceled: **{}**{}-**{}**{}: {} - {}. ({})'.format(self.lastCancelled.teamA, self.lastCancelled.teamAisKnown, self.lastCancelled.teamB,self.lastCancelled.teamBisKnown, self.lastCancelled.scoreA, self.lastCancelled.scoreB, a[0])
            },
        'status': {
            'is': lambda m: self.genericReaction(m, r"^status$"),
            'do': lambda *a: f"""
```
lastValid = {self.lastValid} 
lastCancelled = {self.lastCancelled}
toBeConfirmed = {self.toBeConfirmed}
TTL = {None if self.toBeConfirmed is None else self.toBeConfirmed.TTL}
testing = {self.testing}
running_on = {platform.system()}-{platform.release()}
latest_commit = {subprocess.Popen(['git', 'log', '-1', '--format=%cd'],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")}
```
"""
            },
        'all-time': {
            'is': lambda m: self.genericReaction(m, r"^all-time$"),
            'do': lambda *a: self.ranking()
            },
        'today': {
            'is': lambda m: self.genericReaction(m, r"^today$"),
            'do': lambda *a: self.ranking(24)
            },
        'games': {
            'is': lambda m: self.genericReaction(m, r"^games$"),
            'do': lambda *a: self.games(24)
            },
        'all-games': {
            'is': lambda m: self.genericReaction(m, r"^all-games$"),
            'do': lambda *a: self.games()
            },
        'help': {
            'is': lambda m: self.genericReaction(m, r"^help$"), 
            'do': lambda *a: """
`teamA - teamB X-Y | teamA teamB X-Y | X-Y`: Register game
`ok | yes | y`: Confirm result
`cancel | no | n`:Cancel result
`all-time`: All time standings
`today`: Today's standings
`games`: Today's games
`h2h teamA teamB | h2h teamA-teamB| h2h`: Head to Head all-time`
`help`: This message
`status`: Status"""
            },
        'h2h': {
            'is': self._isH2H,
            'do': lambda *a: self.h2h(self.toReport.teamA, self.toReport.teamB)
            },
    }

        
    def parseMessage(self,message_content):
        """
        returns the answer to bot
        """
        for (key, r) in self.reactions.items():
        ## Go through all registere reactions:
            if r['is'](message_content):
                # If I should react: (is)
                if key == 'yes':
                    #Special case for yes
                    self.toBeConfirmed.confirm()
                    self.lastValid = self.toBeConfirmed
                    self.toBeConfirmed = None
                if key == 'no':
                    #Special case for no
                    self.lastCancelled = self.toBeConfirmed
                    self.toBeConfirmed = None
                    return r['do']('User cancelled')
                #Applies to any other reaction:
                return r['do']()
        # TTL for confirmations (in case none of the other reactions apply):
        self.toBeConfirmed.TTL = self.toBeConfirmed.TTL - 1
        if self.toBeConfirmed.TTL == 0:
            self.lastCancelled = self.toBeConfirmed
            self.toBeConfirmed = None
            return self.reactions['no']['do']('No confirmation received')
        return None
    



#### Reactions

    def genericReaction(self, message, *list_of_triggers):
        for t in list_of_triggers: 
            search_result = re.search(t, message.lower())
            if search_result is not None:
                return True
        return False

    
    
    def _isResult(self,message):
        results = [
            #TeamA - TeamB 4-2
            r"^\s*(\S+)[\s-]+(\S+)\s*(\d+)[\s-]+(\d+)",
            #3 - 2. Should assume the previous teams
            r"^(\d+)[-\s]+(\d+)$",
        ]
        for r in results:
            search_result = re.search(r,message)
            if search_result is not None:
                x = search_result.groups()
                print("Results matched:",x)
                if len(x) == 2 and self.lastValid is not None:
                    self.toBeConfirmed = Validator(self.lastValid.teamA, self.lastValid.teamB, int(x[0]), int(x[1]), self.tournament)
                    return True
                elif len(x) == 4:
                    self.toBeConfirmed = Validator(x[0].strip(), x[1].strip(), int(x[2]), int(x[3]), self.tournament)
                    return True
        return False
    
    def _isH2H(self,message):
        results = [
            #TeamA - TeamB 4-2
            r"^h2h(\s+(\S+)[\s-]+(\S+))?",
        ]
        for r in results:
            search_result = re.search(r,message)
            if search_result is not None:
                x = search_result.groups()
                print("Report H2H matched:",x)
                if x==(None, None, None) and self.lastValid is not None:
                    self.toReport = Validator(self.lastValid.teamA, self.lastValid.teamB, 0, 0, self.tournament)
                    return True
                elif len(x) == 3:
                    #A B, A, B. We need the last 2 elements of this
                    self.toReport = Validator(x[1].strip(), x[2].strip(), 0, 0, self.tournament)
                    return True
        return False

    def ranking(self, hours = None):
        if hours is None:
            standings = self.tournament.getRanking()
            elos = self.tournament.getELOs()
        else:
            standings = self.tournament.getRanking(hours)
            elos1 = self.tournament.getELOs()
            elos2 = self.tournament.getELOs(before_hours = 48)
            elos = elos1.copy()
            print(elos1)
            print(elos2)
            for key in elos1.keys():
                if key in elos2.keys():
                    elos[key]['R'] = elos1[key]['R'] - elos2[key]['R']
                else:
                    elos[key]['R'] = elos1[key]['R']
        
        print(elos)
        response ="\n     {T:10} {M:>2} {W:>2} {D:>2} {L:>2} {GF:>3} {GA:>3} {P:>3} {E:>5}".format(
            T="Team",
            M="M", 
            W="W", 
            D="D", 
            L="L", 
            GF="GF", 
            GA="GA", 
            P="P", 
            E="ELO")
        c = 1
        ordered_standings = sorted(standings, key=lambda k: elos[k[0]]['R'], reverse=True)
        for line in ordered_standings:
            format_line = "\n{C:3}. {T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3} "
            if hours is None:
                format_line +="{E:5}"
            else:
                format_line +="{E:+5}"

            response += format_line.format(
                C=c,
                T=line[0],
                M=line[1]['w']+line[1]['d']+line[1]['l'], 
                W=line[1]['w'], 
                D=line[1]['d'], 
                L=line[1]['l'], 
                GF=line[1]['gf'], 
                GA=line[1]['ga'], 
                P=line[1]['p'], 
                E=elos[line[0]]['R'])
            c+=1
        return f"```{response}```"
    
    def h2h(self, teamA, teamB, hours = 0):
        standings = self.tournament.getRanking(hours, [teamA, teamB])
        response ="\n     {T:10} {M:>2} {W:>2} {D:>2} {L:>2} {GF:>3} {GA:>3} {P:>3}".format(T="Team",M="M", W="W", D="D", L="L", GF="GF", GA="GA", P="P")
        c = 1
        for line in standings:
            response +=  "\n{C:3}. {T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3}".format(C=c,T=line[0],M=line[1]['w']+line[1]['d']+line[1]['l'], W=line[1]['w'], D=line[1]['d'], L=line[1]['l'], GF=line[1]['gf'], GA=line[1]['ga'], P=line[1]['p'])
            c+=1
        return f"```{response}```"
    
    def games(self, hours = None):
        max_games_shown = 50
        if hours is None:
            games = self.tournament.getGames()
            since = "ever"
        else:
            games = self.tournament.getGames(hours)
            since = f"in the last {hours} hours"
        if len(games) == 0:
            response = f"No games {since}."
        else:
            if len(games) < max_games_shown:
                max_games_shown = len(games)
            response = f"{len(games)} games {since}. Showing most recent {max_games_shown}:"

        for line in games[-max_games_shown:]:
            response += "\n{ID:4}. {D:10}:  {T1:>10} {S1} - {S2} {T2:<10}".format(ID=line[0],D=time.ctime(float(line[1])), T1=line[2], T2=line[3], S1=line[4], S2=line[5])
        return f"```{response}```"

