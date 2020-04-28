import re
import time

class Validator:
    def __init__(self, teamA, teamB, scoreA, scoreB, tournament):
        self.teamA = teamA
        self.teamB = teamB
        self.scoreA = scoreA
        self.scoreB = scoreB
        self.validated = False
        self.TTL = 3
        self.tournament = tournament
        self.gameId = None
    def confirm(self):
        self.validated = True
        if self.tournament is not None:
            self.gameId = self.tournament.addGame(self.teamA, self.teamB, self.scoreA, self.scoreB)
            print("Adding game:", self.gameId, self)
        return self.gameId
    def __str__(self):
        return "{}-{} {}-{}.".format(self.teamA, self.teamB, self.scoreA, self.scoreB)


class BotPlatform:
    def __init__(self, tournament = None):
        self.tournament = tournament
        self.lastValid = None
        self.lastCancelled = None
        self.toBeConfirmed = None
        self.reactions = ["RESULT", "YES", "NO", "QUERY", "STATS", "LIST", "TODAY"]
        
    def parseMessage(self,message_content):
        """
        returns the answer to bot
        """
        if self._isResult(message_content):
            return self.reactions[0]
        elif self._isConfirmation(message_content):
            self.toBeConfirmed.confirm()
            self.lastValid = self.toBeConfirmed
            self.toBeConfirmed = None
            return self.reactions[1]
        elif self._isCancelation(message_content):
            self.lastCancelled = self.toBeConfirmed
            self.toBeConfirmed = None
            return self.reactions[2]
        elif self._isQuery(message_content):
            return "QUERY"
        elif self._isStats(message_content):
            return "STATS"
        elif self._isList(message_content):
            return "LIST"
        elif self._isToday(message_content):
            return "TODAY"
        elif self._isHelp(message_content):
            return "HELP"
        else:
            return "Don't care"
    
    def reaction(self,parsed_message ):
        if parsed_message == self.reactions[1]:
            return 'Added #{}: **{}**-**{}**: {}-{}'.format(self.lastValid.gameId,self.lastValid.teamA, self.lastValid.teamB, self.lastValid.scoreA, self.lastValid.scoreB, )
        elif parsed_message == self.reactions[2]:
            return 'Canceled: "{}"-"{}": "{}" - "{}"'.format(self.lastCancelled.teamA, self.lastCancelled.teamB, self.lastCancelled.scoreA, self.lastCancelled.scoreB)
        elif parsed_message == self.reactions[0]:
            return '"{}"-"{}": "{}" - "{}" ? Please confirm'.format(self.toBeConfirmed.teamA, self.toBeConfirmed.teamB, self.toBeConfirmed.scoreA, self.toBeConfirmed.scoreB)
        elif parsed_message == "QUERY":
            return f"""
            ```
            lastValid = {self.lastValid} 
            lastCancelled = {self.lastCancelled}
            toBeConfirmed = {self.toBeConfirmed}
            ```
            """
        elif parsed_message == "STATS":
            response = "```"
            response = response + "\n{T:10} {M:>2} {W:>2} {D:>2} {L:>2} {GF:>3} {GA:>3} {P:>3}".format(T="Team",M="M", W="W", D="D", L="L", GF="GF", GA="GA", P="P")
            for line in self.tournament.getRanking():
                response = response +  "\n{T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3}".format(T=line[0],M=line[1]['w']+line[1]['d']+line[1]['l'], W=line[1]['w'], D=line[1]['d'], L=line[1]['l'], GF=line[1]['gf'], GA=line[1]['ga'], P=line[1]['p'])
            response = response + "\n```"
            return response
        elif parsed_message == "LIST":
            response = "```"
            for line in self.tournament.getGames(24):
                response = response +  "\n{ID:4}. {D:10}:  {T1:>10} {S1} - {S2} {T2:<10}".format(ID=line[0],D=time.ctime(float(line[1])), T1=line[2], T2=line[3], S1=line[4], S2=line[5])
            response = response + "\n```"
            return response
        elif parsed_message == "HELP":
            response = """
```
teamA - teamB x-y | x-y
ok | yes | y
cancel | no | n
all-time
today
games
help
status
```            
            """
            return response
        elif parsed_message == "TODAY":
            response = "```"
            response = response + "\n{T:10} {M:>2} {W:>2} {D:>2} {L:>2} {GF:>3} {GA:>3} {P:>3}".format(T="Team",M="M", W="W", D="D", L="L", GF="GF", GA="GA", P="P")
            for line in self.tournament.getRanking(24):
                response = response +  "\n{T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3}".format(T=line[0],M=line[1]['w']+line[1]['d']+line[1]['l'], W=line[1]['w'], D=line[1]['d'], L=line[1]['l'], GF=line[1]['gf'], GA=line[1]['ga'], P=line[1]['p'])
            response = response + "\n```"
            return response
        self.toBeConfirmed.TTL = self.toBeConfirmed.TTL - 1
        if self.toBeConfirmed.TTL == 0:
            self.lastCancelled = self.toBeConfirmed
            self.toBeConfirmed = None          
            return "Canceled. No confirmation received for: {}-{} {}-{}".format(self.lastCancelled.teamA, self.lastCancelled.teamB, self.lastCancelled.scoreA, self.lastCancelled.scoreB)
        
    
    def _isResult(self,message):
        results = [
            #TeamA - TeamB 4-2
            r"^\w*?(.+?)-(.+?)\w*?(\d+)\w*?-\w*?(\d+)",
            #3 - 2. Should assume the previous teams
            r"^(\d+)\w*?-\w*?(\d+)$",
            #r"^(\d+)-(\d+)$"
        ]
        for r in results:
            search_result = re.search(r,message)
            if search_result is not None:
                x = search_result.groups()
                if len(x) == 2 and self.lastValid is not None:
                    self.toBeConfirmed = Validator(self.lastValid.teamA, self.lastValid.teamB, int(x[0]), int(x[1]), self.tournament)
                    return True
                elif len(x) == 4:
                    self.toBeConfirmed = Validator(x[0].strip(), x[1].strip(), int(x[2]), int(x[3]), self.tournament)
                    return True
        return False
    def _isConfirmation(self, message):
        confirmations = [
            # y, yes
            r"^(yes|y)$",
            r"^(ok)$"
        ]
        for r in confirmations: 
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False
    def _isCancelation(self, message):
        cancelations = [
            # n, no
            r"^(no?)$",
            #cancel
            r"^(cancel)$"
        ]
        for r in cancelations:
            search_result = re.search(r,message)
            if search_result is not None:
                return True
        return False    
    def _isQuery(self, message):
        cancelations = [
            # status
            r"^status$",
        ]
        for r in cancelations:
            search_result = re.search(r,message)
            if search_result is not None:
                return True
        return False
    
    def _isStats(self, message):
        stats = [
            #clasament
            r"^all-time$",
        ]
        for r in stats:
            search_result = re.search(r,message)
            if search_result is not None:
                return True
        return False
    
    def _isList(self, message):
        stats = [
            #games
            r"^games$",
        ]
        for r in stats:
            search_result = re.search(r,message)
            if search_result is not None:
                return True
        return False
    def _isToday(self, message):
        stats = [
            #games
            r"^today$",
        ]
        for r in stats:
            search_result = re.search(r,message)
            if search_result is not None:
                return True
        return False
    def _isHelp(self, message):
        stats = [
            #games
            r"^help$",
        ]
        for r in stats:
            search_result = re.search(r,message)
            if search_result is not None:
                return True
        return False