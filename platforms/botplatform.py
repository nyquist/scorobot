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
        
    def parseMessage(self,message_content):
        """
        returns the answer to bot
        """
        if self._isResult(message_content):
            return self._onResult()
        elif self._isConfirmation(message_content):
            self.toBeConfirmed.confirm()
            self.lastValid = self.toBeConfirmed
            self.toBeConfirmed = None
            return self._onConfirmation()
        elif self._isCancellation(message_content):
            self.lastCancelled = self.toBeConfirmed
            self.toBeConfirmed = None
            return self._onCancellation("User cancelled")
        elif self._isStatus(message_content):
            return self._onStatus
        elif self._isAllTime(message_content):
            return self._onAllTime
        elif self._isGames(message_content):
            return self._onGames()
        elif self._isToday(message_content):
            return self._onToday()
        elif self._isHelp(message_content):
            return self._onHelp()

        self.toBeConfirmed.TTL = self.toBeConfirmed.TTL - 1
        if self.toBeConfirmed.TTL == 0:
            self.lastCancelled = self.toBeConfirmed
            self.toBeConfirmed = None
            return self._onCancellation("No confirmation received.")
        return None
    
        
    
    def _isResult(self,message):
        results = [
            #TeamA - TeamB 4-2
            r"^\s*(\S+)\s*[ -]+\s*(\S+)\s*(\d+)[ -]+(\d+)",
            #3 - 2. Should assume the previous teams
            r"^(\d+)\w*?-\w*?(\d+)$",
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
    def _onResult(self):
        return 'Added #{}: **{}**-**{}**: {}-{}'.format(self.lastValid.gameId,self.lastValid.teamA, self.lastValid.teamB, self.lastValid.scoreA, self.lastValid.scoreB, )

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
    def _onConfirmation(self):
        return '"{}"-"{}": "{}" - "{}" ? Please confirm'.format(self.toBeConfirmed.teamA, self.toBeConfirmed.teamB, self.toBeConfirmed.scoreA, self.toBeConfirmed.scoreB)

    def _isCancellation(self, message):
        cancellations = [
            # n, no
            r"^(no?)$",
            #cancel
            r"^(cancel)$"
        ]
        for r in cancellations:
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False    
    def _onCancellation(self, reason = ""):
        return 'Canceled: "{}"-"{}": "{}" - "{}". ({})'.format(self.lastCancelled.teamA, self.lastCancelled.teamB, self.lastCancelled.scoreA, self.lastCancelled.scoreB, reason)

    def _isStatus(self, message):
        cancellations = [
            # status
            r"^status$",
        ]
        for r in cancellations:
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False
    def _onStatus(self):
        return f"""
            ```
            lastValid = {self.lastValid} 
            lastCancelled = {self.lastCancelled}
            toBeConfirmed = {self.toBeConfirmed}
            ```
            """

    def _isAllTime(self, message):
        stats = [
            #clasament
            r"^all-time$",
        ]
        for r in stats:
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False
    def _onAllTime(self):
        response = "```"
        response = response + "\n{T:10} {M:>2} {W:>2} {D:>2} {L:>2} {GF:>3} {GA:>3} {P:>3}".format(T="Team",M="M", W="W", D="D", L="L", GF="GF", GA="GA", P="P")
        for line in self.tournament.getRanking():
            response = response +  "\n{T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3}".format(T=line[0],M=line[1]['w']+line[1]['d']+line[1]['l'], W=line[1]['w'], D=line[1]['d'], L=line[1]['l'], GF=line[1]['gf'], GA=line[1]['ga'], P=line[1]['p'])
        response = response + "\n```"
        return response

    def _isGames(self, message):
        stats = [
            #games
            r"^games$",
        ]
        for r in stats:
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False
    
    def _onGames(self):
        response = "```"
        for line in self.tournament.getGames(24):
            response = response +  "\n{ID:4}. {D:10}:  {T1:>10} {S1} - {S2} {T2:<10}".format(ID=line[0],D=time.ctime(float(line[1])), T1=line[2], T2=line[3], S1=line[4], S2=line[5])
        response = response + "\n```"
        return response

    def _isToday(self, message):
        stats = [
            #games
            r"^today$",
        ]
        for r in stats:
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False
    def _onToday(self):
        response = "```"
        response = response + "\n{T:10} {M:>2} {W:>2} {D:>2} {L:>2} {GF:>3} {GA:>3} {P:>3}".format(T="Team",M="M", W="W", D="D", L="L", GF="GF", GA="GA", P="P")
        for line in self.tournament.getRanking(24):
            response = response +  "\n{T:10} {M:2} {W:2} {D:2} {L:2} {GF:3} {GA:3} {P:3}".format(T=line[0],M=line[1]['w']+line[1]['d']+line[1]['l'], W=line[1]['w'], D=line[1]['d'], L=line[1]['l'], GF=line[1]['gf'], GA=line[1]['ga'], P=line[1]['p'])
        response = response + "\n```"
        return response

    def _isHelp(self, message):
        stats = [
            #games
            r"^help$",
        ]
        for r in stats:
            search_result = re.search(r,message.lower())
            if search_result is not None:
                return True
        return False
    def _onHelp(self):
        response = """
            ```
            teamA - teamB x-y | x-y
            teamA teamB x y
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