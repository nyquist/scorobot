class Game:
    def __init__(self, player1, player2):
        self._players = (player1, player2)
        self._scores = []
    def get_players(self):
        return self._players
    def add_score(self, score1, score2):
        self._scores.append((score1, score2))
    def get_scores(self, last = False):
        # when last = 0, return all
        if not last:
            return self._scores
        else:
            return self._scores[-last:]
    @staticmethod
    def _compute_stats(scores):
        #          W,D,L,GS,GC
        player1 = [0,0,0,0,0]
        player2 = [0,0,0,0,0]
        
        for score in scores:
            if score[0] > score[1]:
                player1[0] = player1[0] + 1
                player2[2] = player2[2] + 1
            elif score[0] < score[1]:
                player1[2] = player1[2] + 1
                player2[0] = player2[0] + 1
            else:
                player1[1] = player1[1] + 1
                player2[1] = player2[1] + 1
            player1[3] = player1[3] + score[0]
            player2[3] = player2[3] + score[1]
            player1[4] = player1[4] + score[1]
            player2[4] = player2[4] + score[0]
        return (player1, player2)
    def get_stats(self, last = False):
        return self._compute_stats(self.get_scores(last))

if __name__ == '__main__':
    game = Game("Player1", "Player2")
    game.add_score(1,2)
    game.add_score(2,2)
    game.add_score(3,0)
    game.add_score(5,2)
    print("Players: {} - {}".format(game.get_players()[0], game.get_players()[1]))
    print("Last Score: {}".format(game.get_scores(1)))
    print("Last 2 Scores: {}".format(game.get_scores(2)))
    print("All Scores: {}".format(game.get_scores()))
    print("last 2 Stats: {}".format(game.get_stats(2)[0]))
    print("All Stats: {}".format(game.get_stats()[0]))