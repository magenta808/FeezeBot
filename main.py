import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'We Have logged in as Feeze Bot')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('when'):
        await message.channel.send('i say feeze, you say:')

client.run('TOKEN')
