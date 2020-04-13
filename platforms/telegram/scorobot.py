from telegram.ext import Updater, CommandHandler
import telegram
import configparser
from game import Game
import logging

        

def score(bot, update, args):
    print (args)
    wrong_cmd = "Unknown command: '{}'.Supported commands: who, add, last [N], stats [N]".format(args[0])
    if args[0] == "who":
        players_list = game.get_players()
        msg = "Now playing: {} - {}".format(players_list[0], players_list[1])
    elif args[0] == "add":
        scor = args[1].split('-')
        if len(scor) != 2:
            msg = "Wrong format. Use /score add x-y."
        else:
            game.add_score(int(scor[0]),int(scor[1]))
            msg = "Added score {}-{}".format(int(scor[0]), int(scor[1]))
    elif args[0] == "stats":
        if len(args) > 1:
            stats = game.get_stats(int(args[1]))[0]
        else:
            stats = game.get_stats()[0]
        msg = stats
    elif args[0] == "last":
        if len(args) > 1:
            scores = game.get_scores(int(args[1]))
        else:
            scores = game.get_scores()
        msg = scores
    else:
        msg = wrong_cmd

    update.message.reply_text(
        'Hello {}! {}'.format(update.message.from_user.first_name, msg))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
config = configparser.ConfigParser()

with open('scorobot.cfg', mode ="r") as fh:
    config.read_file(fh)
    fh.close()

updater = Updater(config['Bot']['Token'],  )
game = Game(config['Bot']['TeamA'],config['Bot']['TeamB'])

updater.dispatcher.add_handler(CommandHandler('score', score, pass_args=True))



updater.start_polling()
print ("Dispatcher Ready")
updater.idle()