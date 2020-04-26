import re

class BotPlatform:
    def __init__(self):
        self.lastTeamA = None
        self.lastTeamB = None
        self.toBeConfirmed = None
        
    def parseMessage(self,message_content):
        confirmations = [
            # y, yes
            r"(^y[es]?$^)",
            r"(^ok$)"
        ]
        cancelations = [
            # n, no
            r"^no?$",
            #cancel
            r"^cancel$"
        ]
        results = [
            #TeamA - TeamB 4-2
            r"^\w*?(.+?)-(.+?)\w*?(\d+)\w*?-\w*?(\d+)",
            #3 - 2. Should assume the previous teams
            r"^(\d+)\w*?-\w*?(\d+)$",
        ]
        for r in results:
            search_result = re.search(r,message_content)
            if search_result is not None:
                x = search_result.groups()
                print(x)
                if len(x) == 2 or len(x) == 4:
                    try:
                        teamA = x[0] if len(x) == 4 else self.lastTeamA
                        teamB = x[1] if len(x) == 4 else self.lastTeamB
                        scoreA = int(x[2]) if len(x) == 4 else int(x[0])
                        scoreB = int(x[3]) if len(x) == 4 else int(x[1])
                        if teamA is None or teamB is None:
                            return ('error', "Unknown teams")
                        self.lastTeamA = teamA
                        self.lastTeamB = teamB
                        return ('result',teamA, teamB, scoreA, scoreB)
                    except Exception as e:
                        print(e)
        for r in confirmations: 
            search_result = re.search(r,message_content)
            if search_result is not None:
                x = search_result.groups()
                print(x)
                if re.search(r, message_content.lower()).groups():
                    return ('confirmation', True)
        for r in cancelations:
            search_result = re.search(r,message_content)
            if search_result is not None:
                x = search_result.groups()
                print(x)
                if re.search(r, message_content.lower()).groups():
                    return ('confirmation', False)
        return None
    
    def reaction(self,parsed_message):
        if parsed_message is None:
            return None
        if parsed_message[0] == 'result':
            return "{}-{}: {} - {} ? Please confirm".format(parsed_message[1], parsed_message[2], parsed_message[3], parsed_message[4])
        if parsed_message[0] == 'confirmation':
            if parsed_message[1]:
                return "Acknowledged. I will proceed."
            else:
                return "Canceling."
        if parsed_message[0] == 'error':
            return "Oops.. {}".format(parsed_message[1])
    
     
