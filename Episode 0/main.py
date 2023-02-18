import discord 
from discord.ext import commands 
import asyncio 

client = commands.Bot(command_prefix="!") # modify the prefix here 

@client.event 
async def on_ready(): # When the bot is online
    print("Bot Ready !")
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Cool Music !")) # "Listening to Cool Music !" < in status

client.run("NzIyNzMxMzk1NDU3NDgyNzUz.GZmnJd.kbT9VK7fMBAqD9ltNNKZmpF03GqiYjZ_o9-X2U")
