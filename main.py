# Referenced
# https://realpython.com/how-to-make-a-discord-bot-python/

import os
import re

from dotenv import load_dotenv
from discord.ext import commands
from runcode import CodeDriver, CodeDriverSecure


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

# Empty for now...



#############################################################################
#                                                                           #
#                            Command Functions                              #
#                                                                           #
#############################################################################

# The `code` command, used to run code based on user input
# Extracts the code contained in `arg` and formats the response
@bot.command(name='code', aliases=['c', 'comp'], 
help='''
Runs the code inputed in the language specified. 
Can also be invoked by `c` or `comp`.

CodeBot currently supports the following languages:
    Bash        (bash)
    C           (c)
    C++         (c++)
    Java        (java)
    JavaScript  (javascript, js)
    Python      (python)
    SML/NJ      (sml)

To run code in one of these languages run the following command, replacing `lang` with the string in parenthesis above corresponding to your desired language:
>code `​`​`lang
input your code here
`​`​`
''')
async def code(ctx, *, arg=""):

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
            driver = CodeDriverSecure()
            exit_status, output, error = driver.run(lang, code)
            
            response = "**Exit Status:** " + str(exit_status) + "\n"

            if (len(output.strip()) > 0):
                response += "**Output:**\n```\n" + output + "\n```"

            if (len(error.strip()) > 0):
                response += "**Errors:**\n```\n" + error + "\n```"

    await ctx.reply(response)

'''
# The `again` command, used to re-run the user's most recent `code` command in the 
# channel the user used to call the `again` command
@bot.command(name='code', aliases=['c', 'comp'], help='')
async def again(ctx):
'''


# Runs the bot
bot.run(TOKEN)



