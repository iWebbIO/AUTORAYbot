import discord
import requests
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
apiSecret = "ql1lGsB7TTO3TOOR2vRjaMgQi2DvmEWtngOkxNtFhTLQaDUne6sZvhRhD0jXUAKC0DtL9EW8fCZO5GdzHaIZyuBM2Re2OdYi"
tvcbaseurl = "HOST:IP"
endpoint = "HOST:IP"
APIE = {
    key_list : f"{endpoint}/allkeys?key={apiSecret}"
    new_key : f"{endpoint}/createkey?pass={apiSecret}"
    append_key : f"{endpoint}/addkey?key={apiSecret}&tkey="
    delete_key : f"{endpoint}/delkey?key={apiSecret}&tkey="
    ping : f"{endpoint}/ping?key={apiSecret}"
}
bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())

admins = []
allowedChannels = []


@bot.event
async def on_ready():
    print("AutorayBot by iWebbIO\nv0.9.1-SR\nReport bugs/issues on github.com/iWebbIO/AUTORAYbot\nAUTORAYbot is READY!")
    print(f'Logged in as {bot.user.name}')
    if admins == []:
        print("No AUTORAYbot managers have been specified!\nEdit the 'admins' variable to configure your admins")
    if allowedChannels == []:
        print("No AUTORAYbot allowed channels have been specified!\nEdit the 'allowedChannels' variable to configure your allowed channels")

@bot.command()
@commands.guild_only()
async def key(ctx):
    if ctx.author.id in admins:
        resultkey = requests.get(APIE[new_key])
        await ctx.send(f"{resultkey.text}\nRequested by: {ctx.message.author.mention}")
@bot.command(name="ping")
@commands.guild_only()
async def pingcommand(ctx):
    result = requests.get(APIE[ping])
    ctx.send(f"Discord Bot: `ALIVE`\nVPN: `{result.text}`")
@bot.command()
@commands.guild_only()
async def keylist(ctx):
    if ctx.author.id in admins:
         result = requests.get(APIE[key_list])
         await ctx.send(f"List of all active keys:\n```{result.text}```\nRequested by: {ctx.message.author.mention}")

@bot.command()
@commands.guild_only()
async def delkey(ctx):
    try:
        if ctx.author.id in admins:
            deleterequest = requests.get(APIE[delete_key] + ctx.message.content.split(" ")[1])
            await ctx.reply(f"Request sent :white_check_mark: \nResult: `{deleterequest.text}`\nRequested by: {ctx.message.author.mention}")
    except:
        await ctx.send("CRITICAL ERR")
@bot.command()
@commands.guild_only()
async def addkey(ctx):
    try:
        addrequest = requests.get(APIE[append_key] + ctx.message.content.split(" ")[1])
        await ctx.reply(f"Request sent :white_check_mark: \nResult: `{addrequest.text}`\nRequested by: {ctx.message.author.mention}")

    except:
        await ctx.send("CRITICAL ERR")
@bot.event
async def on_message(ctx):
    if ctx.guild:
        await bot.process_commands(ctx)
    else:
        await ctx.send("Access Denied! Use the discord server")

bot.run('DISCORD-BOT-TOKEN')
