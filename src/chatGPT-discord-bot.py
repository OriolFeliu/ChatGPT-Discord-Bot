import discord


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hi there!')

client.run(
    'MTEwMDA3ODM4NjQ3MjI4ODMyNg.G0LBg4.zxjIMsTGciAlNY034hXIDo15ezP3olHc0E0mgM')
