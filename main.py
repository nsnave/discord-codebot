# Referenced
# https://realpython.com/how-to-make-a-discord-bot-python/

import os
import re

from dotenv import load_dotenv
from discord.ext import commands
from runcode import CodeDriver


# Loads dotenv (used to get env variables)
load_dotenv()

# Gets the BashBot Discord Token env variable
TOKEN = os.getenv('DISCORD_CODEBOT_TOKEN')



#############################################################################
#                                                                           #
#                               Bot Setup                                   #
#                                                                           #
#############################################################################

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



#############################################################################
#                                                                           #
#                            Command Utilities                              #
#                                                                           #
#############################################################################

# Runs the code contained in `arg` and formats the response
def processCode(arg):
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

    return response



#############################################################################
#                                                                           #
#                            Command Functions                              #
#                                                                           #
#############################################################################

# The `code` command, used to run code based on user input
@bot.command(name='code', help='Runs the code inputed in the language specified.')
async def code(ctx, *, arg=""):
    await ctx.send(processCode(arg))
    

@bot.command(name='c', help='The same as `code`.')
async def c(ctx, *, arg=""):
    await ctx.send(processCode(arg))
    




# Runs the bot
bot.run(TOKEN)



