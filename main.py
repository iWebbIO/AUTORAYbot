import discord
import requests
from discord.ext import commands, tasks
from datetime import datetime
import asyncio

# API Credentials and URLs
apiSecret = "ql1lGsB7TTO3TOOR2vRjaMgQi2DvmEWtngOkxNtFhTLQaDUne6sZvhRhD0jXUAKC0DtL9EW8fCZO5GdzHaIZyuBM2Re2OdYi"
tvcbaseurl = "HOST:IP"
endpoint = "HOST:IP"
APIE = {
    "key_list": f"{endpoint}/allkeys?key={apiSecret}",
    "new_key": f"{endpoint}/createkey?pass={apiSecret}",
    "append_key": f"{endpoint}/addkey?key={apiSecret}&tkey=",
    "delete_key": f"{endpoint}/delkey?key={apiSecret}&tkey=",
    "ping": f"{endpoint}/ping?key={apiSecret}",
}

# Bot Configuration
bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())
admins = []  # List of authorized admin user IDs
allowedChannels = []  # List of authorized channels for bot commands

# Bot Events

@bot.event
async def on_ready():
    """Prints bot information and checks for configuration."""
    print("AutorayBot by iWebbIO")
    print("v0.9.1-SR")
    print("Report bugs/issues on github.com/iWebbIO/AUTORAYbot")
    print(f'Logged in as {bot.user.name}')

    if not admins:
        print("No admins configured! Edit the 'admins' variable.")
    if not allowedChannels:
        print("Bot will not restrict itself to specific channels.")

@bot.command()
@commands.guild_only()
async def key(ctx):
    """Generates a new key if the user is an admin."""
    if ctx.author.id in admins:
        try:
            result = requests.get(APIE['new_key'])
            await ctx.send(f"{result.text}\nRequested by: {ctx.message.author.name}")  # Removed mention
        except Exception as e:
            await ctx.send(f"Error generating key: {e}")

@bot.command(name="ping")
@commands.guild_only()
async def pingcommand(ctx):
    """Pings the VPN and Discord bot."""
    try:
        result = requests.get(APIE['ping'])
        await ctx.send(f"Discord Bot: `ALIVE`\nVPN: `{result.text}`")
    except Exception as e:
        await ctx.send(f"Error pinging: {e}")

@bot.command()
@commands.guild_only()
async def keylist(ctx):
    """Lists all active keys if the user is an admin."""
    if ctx.author.id in admins:
        try:
            result = requests.get(APIE['key_list'])
            await ctx.send(f"List of all active keys:\n```{result.text}```\nRequested by: {ctx.message.author.name}")  # Removed mention
        except Exception as e:
            await ctx.send(f"Error fetching key list: {e}")

@bot.command()
@commands.guild_only()
async def delkey(ctx):
    """Deletes a key if the user is an admin and provides a valid key."""
    if ctx.author.id in admins:
        try:
            key_to_delete = ctx.message.content.split(" ")[1]
            result = requests.get(APIE['delete_key'] + key_to_delete)
            await ctx.reply(f"Request sent :white_check_mark: \nResult: `{result.text}`\nRequested by: {ctx.message.author.name}")  # Removed mention
        except Exception as e:
            await ctx.send(f"Error deleting key: {e}")

@bot.command()
@commands.guild_only()
async def addkey(ctx):
    """Adds a key if the user is an admin and provides a valid key."""
    if ctx.author.id in admins:
        try:
            key_to_add = ctx.message.content.split(" ")[1]
            result = requests.get(APIE['append_key'] + key_to_add)
            await ctx.reply(f"Request sent :white_check_mark: \nResult: `{result.text}`\nRequested by: {ctx.message.author.name}")  # Removed mention
        except Exception as e:
            await ctx.send(f"Error adding key: {e}")

@bot.event
async def on_message(ctx):
    """Handles messages and restricts commands to allowed channels if configured."""
    if ctx.guild:
        if allowedChannels:  # Only restrict if allowedChannels is not empty
            if ctx.channel.id not in allowedChannels:
                await ctx.send("This command is not allowed in this channel.")
                return
        await bot.process_commands(ctx)
    else:
        await ctx.send("Access Denied! Use the discord server")

# Run the bot
bot.run('DISCORD-BOT-TOKEN')
