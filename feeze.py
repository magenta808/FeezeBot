from argparse import Action
import discord
import io
import random
import os
import datetime
from discord import app_commands
from discord.utils import utcnow
from discord.ext.commands import Bot
from datetime import datetime, date, time, timezone, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.ext.commands.Bot("$", intents=intents)

HOME = discord.Object(id=1010658349592887336) #the FB test server
GOD = 697905630391959572 #my id

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Feeze Bot Initialization Complete")
    await client.change_presence(activity=discord.Game("Galaxy On Fire 4: Unleashed"))

@client.tree.command() #HELLO
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")

async def calc_timediff(channel: discord.TextChannel): #CALCULATE TIMEDIFF
    last_message_time = await channel.fetch_message(channel.last_message_id)
    timediff = (discord.utils.utcnow() - last_message_time.created_at)
    print(f'calc_timediff = {timediff}')
    return timediff

async def randfreeze(channel: discord.TextChannel): #RETURN RANDOM FREEZE
    arr = os.listdir("//FreezeBot/freezes")
    rando = random.randint(0, 1276)
    randomfreeze = arr[rando]
    rando = str(rando)
    with open(f"//FreezeBot/freezes/{randomfreeze}", "rb") as image:
        with io.BytesIO(image.read()) as imageBytes:
            imageBytes.seek(0)
            randFreeze = discord.File(imageBytes, filename = "randfreeze.jpg")
            return randFreeze

@client.tree.command() #AUTOPOST
async def autopost(interaction: discord.Interaction):
    timediff = await calc_timediff(interaction.channel)
    if timediff < timedelta(minutes = 3):
        await interaction.response.send_message("Abuse of power detected", ephemeral = True)
    else:
        randFreeze = await randfreeze(interaction.channel)
        await interaction.channel.send(file = randFreeze)
        await interaction.response.send_message("Autopost successful", ephemeral = True)

@client.tree.command() #FREEZE
async def freeze(interaction: discord.Interaction):
    randFreeze = await randfreeze(interaction.channel)
    await interaction.response.send_message(file = randFreeze)

@client.tree.command() #SHUTDOWN
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == GOD:
        await interaction.response.send_message("Shutting down...", ephemeral = True)
        await client.close()

client.run(TOKEN)
