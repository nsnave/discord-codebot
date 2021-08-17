# CodeBot
A Discord bot that allows users to run code for various languages in the chat interface.


## Setup
First, a `.env` file needs to be created in the main directory containing an entry for Discord's authorization token as follows:
```
DISCORD_CODEBOT_TOKEN=insert_token_here
```

To start CodeBot, then run `python3 main.py` on a Linux platform.

## Use
Once CodeBot is connected to a server, use `>help` to get more information on executing code. In brief, code is submited to the bot using code blocks in Discord; the code contained within the block is run and the language is declared via the language listed for the code block's highlighting syntax. 


