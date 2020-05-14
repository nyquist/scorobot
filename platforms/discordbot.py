import discord
from dotenv import load_dotenv
from platforms.botplatform import BotPlatform
import os
import re



class DiscordBot(discord.Client, BotPlatform):
    def __init__(self, tournament=None):
        BotPlatform.__init__(self)
        discord.Client.__init__(self)
        self.tournament = tournament
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'{self.user} is connected to the following guild:\n')
        for guild in self.guilds:
            print(f'{guild.name}(id: {guild.id})\n')

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(message.content)  
        print(message.author)  
        print(message.channel)

        received_message = self.parseMessage(message.content)
        if received_message is not None:
            await message.channel.send(received_message)        

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    scorobot = DiscordBot()
    scorobot.run(TOKEN)
