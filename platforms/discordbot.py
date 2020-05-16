import discord
from dotenv import load_dotenv
from platforms.botplatform import BotPlatform
import os
import re



class DiscordBot(discord.Client, BotPlatform):
    def __init__(self, tournament=None, testing = False):
        BotPlatform.__init__(self, testing)
        discord.Client.__init__(self)
        self.tournament = tournament
        self.testing = testing
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'{self.user} is connected to the following guild:\n')
        if self.testing:
            print ('Running in test mode')
        for guild in self.guilds:
            print(f'{guild.name}(id: {guild.id})\n')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(message.content)  
        print(message.author)  
        print(message.channel)
        if (not self.testing and type(message.channel) is discord.channel.TextChannel) or (self.testing and type(message.channel) is discord.channel.DMChannel):
            ## Normal operation - only allow  messages from groups while not testing
            ## Testing mode - only allow direct messages while in testing
            received_message = self.parseMessage(message.content)
            if received_message is not None:
                await message.channel.send(received_message)
            

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    scorobot = DiscordBot()
    scorobot.run(TOKEN)
