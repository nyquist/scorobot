import discord
from dotenv import load_dotenv
import os


class Scorobot(discord.Client):
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
        if message.content.startswith('sb!'):
            await message.channel.send("Here I am")

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    scorobot = Scorobot()
    scorobot.run(TOKEN)
