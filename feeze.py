from argparse import Action
import discord
import io
import random
import os
import datetime
from discord import app_commands
from discord.ext.commands import Bot
from datetime import datetime, date, time, timezone

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.ext.commands.Bot("$", intents=intents)

HOME = discord.Object(id=1010658349592887336) #the FB test server
ACTION_FREEZE = discord.Object() #channel to work in

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Feeze Bot Initialization Complete')
    await client.change_presence(activity=discord.Game('Galaxy On Fire 4: Unleashed'))

@client.tree.command() #HELLO
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command() #FREEZE
async def freeze(interaction: discord.Interaction):
    arr = os.listdir('/FreezeBot/freezes')
    rando = random.randint(0,1276)
    randomfreeze = arr[rando]
    rando = str(rando)
    with open(f'/FreezeBot/freezes/{randomfreeze}', 'rb') as image:
        with io.BytesIO(image.read()) as imageBytes:
            imageBytes.seek(0)
            imageFile = discord.File(imageBytes, filename="freeze.jpg")
            await interaction.response.send_message(f'**{rando}**', file=imageFile)

@client.tree.command() #SETUP
async def setup(interaction: discord.Interaction):
    if interaction.user.id == 697905630391959572:
        ACTION_FREEZE = interaction.channel
        await interaction.response.send_message(f'Setup complete. Posting enabled in {ACTION_FREEZE.mention}.')

@client.tree.command() #AUTOPOST
async def autopost(interaction: discord.Interaction):
    if ACTION_FREEZE.last_message.author == client.user:
        await interaction.response.send_message('Abuse of power is prohibited.')
    else:
        await ACTION_FREEZE.send('THIS IS AN ACTION FREEZE')
        await interaction.response.is_done()

@client.tree.command() #SHUTDOWN
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == 697905630391959572:
        await interaction.response.send_message('Shutting down...')
        await client.close()

client.run(TOKEN)
