import os
import re

from dotenv import load_dotenv
from discord.ext import commands
from runcode import CodeDriver

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
    # Checks that the argument is in the correct format
    if (len(arg) >= 6 and arg[:3] != '```' or arg[-3:] != '```'):
        response = 'Incorrect Comand Syntax: argument must be enclosed by "```".'
    else:
        # Checks that the language is provided in the argument
        lang_temp = re.search('```.+[\n ]', arg)
        if (lang_temp == None):
            response = 'Incorrect Command Syntex: must specify language directly after the left "```".'
        else:
            # Extracts language and code from the argument
            lang = lang_temp.group()[3:-1]
            code = arg[3+len(lang):-3].lstrip()

            # Runs code and formats the output
            exit_status, output, error = CodeDriver.run(lang, code)
            
            response = "**Exit Status:** " + str(exit_status) + "\n"

            if (len(output.strip()) > 0):
                response += "**Output:**\n```\n" + output + "\n```"

            if (len(error.strip()) > 0):
                response += "**Errors:**\n```\n" + error + "\n```"

    await ctx.send(response)
    

bot.run(TOKEN)
