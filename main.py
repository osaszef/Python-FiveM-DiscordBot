import time
import requests
import discord
from discord.ext import commands, tasks
import json


data = json.load(open("config.json"))

#---
discordInfo = data['discordBot']
fivemServer = data['fivemServer']

dcToken = discordInfo[0].get('token')
dcPrefix = discordInfo[0].get('prefix')

serverIP = fivemServer[0].get('serverIP')
serverPort = fivemServer[0].get('serverPort')
slots = fivemServer[0].get('slots')
#---


client = commands.Bot(command_prefix=dcPrefix)

@tasks.loop(seconds=45)
async def status():
    r = requests.get('http://' + serverIP + ":" + serverPort + '/players.json').json()
    all = len(r)
    await client.change_presence(activity=discord.Game(name='Players: [{}/{}]'.format(all, slots)),)

@client.event
async def on_ready():
    print("! <-- BOT IS ONLINE --> !")
    status.start()

@client.command(aliases=['playerlist', 'player_list', 'list'])
async def players(ctx):
    timenow = time.strftime("Today at: %H:%M")
    resp = requests.get('http://' + serverIP + ":" + serverPort + '/players.json').json()
    total_players = len(resp)
    if not total_players:
        await ctx.reply("```Server is empty!```")
    else:
        embed = discord.Embed(title=f"Players - [{total_players}/{slots}]", color=discord.Color.blue())
        embed.set_footer(text=f'osaszef | {timenow}')
        for player in resp:
            embed.add_field(name=f"``[{player['id']}]`` {player['name']} ``Ping: {player['ping']}``", value=f"** **", inline=False)
        await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"**Missing arguments**", mention_author=False)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"**Missing Permissions**", mention_author=False)



client.run(dcToken)