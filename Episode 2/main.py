import discord 
from crtoolkit import JsonData, DatabaseHandler
from discord.ext import commands 
import asyncio 
from random import randint # lib to pick a random number between a and b
client = commands.Bot(command_prefix='!',help_command = None) # modify the prefix here 

def recuperer_toutes_les_sanctions(discord_id):
    # BONUS 1
    db = DatabaseHandler("moderation.db")
    db.connectToDb()
    return db.executeQueries(f"SELECT type,raison FROM sanctions WHERE discordId = {discord_id}")
def ajouter_sanction(discord_id, sanctionType, raison, mod_id):
    db = DatabaseHandler("moderation.db")
    db.connectToDb()
    db.executeQueries(
        f"INSERT INTO sanctions (discordId, type, raison, modId) VALUES ({discord_id},'{sanctionType}','{raison}',{mod_id})"
        )
    db.commitChanges()
    db.closeDb()
    return 1

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
    # BONUS 2 (Help mis à jour)
    embed=discord.Embed(
        title="Page d'aide 1/1",
        description="Vous trouverez ici toutes les commandes du bot !",
        color=0x0AAB1D
    )
    embed.add_field(
        name="Pour lancer un dé",
        value="Faîtes `!dice <number of face>` ou encore `!dé <nombre de faces>`",
        inline = True
    )
    embed.add_field(
        name = "Pour bannir quelqu'un",
        value = "Faîtes `!ban @user <nombre de jours pour supprimer les messages> <Raison>`",
        inline = True
    )
    embed.add_field(
        name = "Pour kick quelqu'un",
        value = "Faîtes `!kick @user <Raison>`",
        inline = True
    )
    await ctx.send(embed=embed)

@client.command(pass_context = True, name = "ban", aliases = ["banuser"])
@commands.has_permissions(ban_members = True) # Peut ban des gens (permissions des rôles Discord)
async def ban (ctx, member : discord.Member, jours : int, *, raison=""):
    await member.ban(reason = raison, delete_message_days = jours)
    e = discord.Embed(
        title = f"{ctx.message.author.name} a été banni du serveur.",
        description = f"Raison du bannissement : {raison}",
        color = 0xff0A00
    )
    e.set_author(name = ctx.message.author.name,icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed=e)

@client.command(pass_context = True, name = "kick", aliases = ["kickuser"])
@commands.has_permissions(kick_members=True) # Peut kick des gens (permissions des rôles Discord)
async def kick (ctx,member : discord.Member, *, raison = ""):
    await member.kick(reason=raison)
    e=discord.Embed(
        title = f"{ctx.message.author.name} a été kick.",
        description = f"Raison du kick : `{raison}`",
        color = 0xFF0500
    )
    e.set_author(name = ctx.message.author.name,icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed=e)
@client.command(pass_context=True, name = "warn", aliases =["avertir","avert"])
@commands.has_permissions(kick_members=True) # Doit pouvoir kick pour pouvoir warn (peut être modifié)
async def warn(ctx,member : discord.Member, warnType, *,msg):
    ajouter_sanction(member.id,"warn",msg,ctx.message.author.id)
    await ctx.send("Sanction envoyée !")

client.run("VOTRE TOKEN")
