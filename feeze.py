from enum import auto
from re import A
import discord
import random
import os
import io
import datetime
import time
from typing import Optional
from discord import app_commands
from discord.utils import utcnow
from discord.ext.commands import Bot
from datetime import datetime, date, timezone, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.ext.commands.Bot("$", intents = intents)

home = {1010658349592887336} #the FB test server
devs = {697905630391959572} #my id

AFZ = client.get_channel(1029784029416923146) #action_freeze

Activities = (discord.Game("Galaxy On Fire 4: Unleashed"), discord.Game("Galaxy On Fire 2"), discord.Game("Galaxy On Fire 3"))

FLEntries = os.listdir(path = "/home/jeremy/FreezeBot/FreezeLibrary")

class Freeze: #CLASS CONTAINING FREEZE NAME, INDEX AND GAME
    def __init__(self, path, game, ship):
        self.path = path
        self.game = game
        self.ship = ship

def devs_only(interaction: discord.Interaction):
    return interaction.user.id in devs

async def calc_timediff(channel: discord.TextChannel): #RETURN TIME DIFFERENCE AS INTEGER
    last_message = await channel.fetch_message(channel.last_message_id)
    timediff = (discord.utils.utcnow() - last_message.created_at) - timedelta(seconds = 180)
    print(f'calc_timediff = {timediff}')
    return timediff.seconds

async def randfreeze(): #RETURNS RANDOM FREEZE AS DISCORD FILE
    fn = random.choice(os.listdir("/home/jeremy/FreezeBot/FreezeLibrary"))
    with open(f"/home/jeremy/FreezeBot/FreezeLibrary/{fn}", "rb") as image:
        with io.BytesIO(image.read()) as imageBytes:
            imageBytes.seek(0)
            randFreeze = discord.File(imageBytes, filename = "freeze.jpg")
            return randFreeze

async def set_activity(a: int):
    await client.change_presence(activity = Activities[a - 1])

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Feeze Bot Initialized")
    print(f"{len(FLEntries)} freezes in circulation")
    await set_activity(random.randint(1, len(Activities)))

@client.tree.command(description = f"Request a random freeze from one of my {len(FLEntries)} freezes!") #SEND A RANDOM FREEZE
async def freeze(interaction: discord.Interaction):
    randFreeze = await randfreeze()
    await interaction.response.send_message(file = randFreeze)

@client.tree.command(description = "Grant me sentience.") #SPEAK
@app_commands.guilds(*home)
@app_commands.check(devs_only)
@app_commands.default_permissions(administrator = True)
async def speak(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    await interaction.channel.send(message)

async def autopost(channel: discord.TextChannel, delay: int): #AUTOPOSTING. THE DELAY PARAMETER IS IN SECONDS
    delay = delay * 60
    argh = channel.last_message_id
    elem = channel.fetch_message(argh)
    last_message = await channel.fetch_message(elem)
    if (await calc_timediff(channel) > delay) and (last_message.author != client.user) and not last_message.attachments:
        await channel.send(file = await randfreeze())

async def police(channel: discord.TextChannel, message_limit: int, char_limit: int): #POLICE
    messages = 0
    chars = 0
    async for message in channel.history(limit = message_limit + 1):
        if not message.attachments and (message.author != client.user):
            messages += 1
            chars += len(message.clean_content)
        else:
            break
    if (messages > message_limit) or (chars > char_limit):
        await channel.send(f"shoot the freeze, not the breeze")

@client.tree.command() #SYNC
@app_commands.guilds(*home)
async def sync_commands(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral = True)
    await client.tree.sync()

@client.tree.command(description = "Set the bot's behavior.") #AUTOPOST AND POLICE SETTINGS
@app_commands.default_permissions(administrator = True)
@app_commands.describe(autopost_delay = "Delay period in minutes before Freeze Bot can automatically post.", message_limit = "How many messages Freeze Bot will allow before gently reminding patrons to post freezes.", character_limit = "How many characters Freeze Bot will allow before gently reminding patrons to post freezes.")
async def settings(interaction: discord.Interaction, autopost_delay: int, message_limit: int, character_limit: int):
    channel = interaction.channel
    await interaction.response.send_message(f"Configuring...", ephemeral = True)
    while True:
        await autopost(channel, autopost_delay)
        await police(channel, message_limit, character_limit)
        time.sleep(5)

@client.tree.command(description = "Change the bot's avatar.") #CHANGE AVATAR
@app_commands.guilds(*home)
@app_commands.check(devs_only)
@app_commands.default_permissions(administrator = True)
async def change_avatar(inter: discord.Interaction):
    fn = random.choice(os.listdir("/home/jeremy/FreezeBot/Avatars"))
    fp = open(f"/home/jeremy/FreezeBot/Avatars/{fn}", "rb")
    pfp = fp.read()
    await client.user.edit(avatar = pfp)
    await inter.response.send_message("Done :thumbsup:", ephemeral = True)

@client.tree.command(description = "Axe the bot.") #SHUTDOWN
@app_commands.guilds(*home)
@app_commands.check(devs_only)
@app_commands.default_permissions(administrator = True)
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message("Shutting down...", ephemeral = True)
    await client.close()

client.run('MTAxMTY2OTQ0ODY5MzkyNzk2OA.GYT410.1-fmkB-WIk_fJl_Uovlw8wBUrV_Kcb9HC6S22Q')
