import os

from dotenv import load_dotenv

from discord.ext import commands

# Loads dotenv (used to get env variables)
load_dotenv()

# Gets the BashBot Discord Token env variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Sets up the bot
bot = commands.Bot(command_prefix='>')

# Handles the on_ready event
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

'''
# Handles the on_member_join event
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
'''

# Handles the command events

@bot.command(name='comp', help='Compiles the code inputed in the language specified.')
async def comp(ctx, *, arg=""):
    response = "test test\n"
    response += arg
    await ctx.send(response)
    

bot.run(TOKEN)
