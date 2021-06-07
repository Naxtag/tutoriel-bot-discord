import discord 
from discord.ext import commands 
import asyncio 
from random import randint # lib to pick a random number between a and b
client = commands.Bot(command_prefix='!',help_command = None) # modify the prefix here 

@client.event 
async def on_ready(): # When the bot is online
    print("Bot Ready !")
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Cool Music !")) # "Listening to Cool Music !" < in status

@client.command(pass_context=True, name = "dice", aliases = ["dé","dés","dices"])
async def dice(ctx,nb:int):
    result = randint(1,nb)
    embed=discord.Embed(
        title = f"Tirage d'un dé de {nb} faces",
        description = f"Le dé tombe sur `{result}` ! ",
        color = 0xAE02A1 # Hex-coded color
    )
    embed.set_author(name = ctx.message.author.name, url = "https://crdev.xyz/",icon_url = ctx.message.author.avatar_url) # adding an author tab
    await ctx.send(embed=embed) # sending an embed not a text (string)


@client.command(pass_context=True,name="help")
async def help(ctx):
    embed=discord.Embed(
        title="Page d'aide 1/1",
        description="Vous trouverez ici toutes les commandes du bot !",
        color=0x0AAB1D
    )
    embed.add_field(
        name="Pour lancer un dé",
        value="Faîtes `!dice <number of face>` ou encore `!dé <nombre de faces>`"
    )
    await ctx.send(embed=embed)

client.run("token")
