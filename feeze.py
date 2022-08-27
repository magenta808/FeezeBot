import discord
import io
import random
import os
from discord import app_commands
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.ext.commands.Bot("$", intents=intents)
HOME = discord.Object(id=1010658349592887336)
ME = 697905630391959572

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Feeze Bot Initialization Complete')

@client.tree.command() #HELLO
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command() #FREEZE
async def freeze(interaction: discord.Interaction):
    arr = os.listdir('/Freeze Bot/freezes')
    rando = random.randint(0,1276)
    randomfreeze = arr[rando]
    rando = str(rando)
    with open(f'/Freeze Bot/freezes/{randomfreeze}', 'rb') as image:
        with io.BytesIO(image.read()) as imageBytes:
            imageBytes.seek(0)
            imageFile = discord.File(imageBytes, filename="freeze.jpg")
            await interaction.response.send_message(f'**{rando}**', file=imageFile)

@client.tree.command() #SHUTDOWN
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == ME:
        await interaction.response.send_message('Shutting down...')
        await client.close()

client.run(TOKEN)
