# CodeBot

A Discord bot that allows users to run code for various languages in the chat interface.

## Setup

First, a `.env` file needs to be created in the main directory containing an entry for Discord's authorization token as follows:

```
DISCORD_CODEBOT_TOKEN=insert_token_here
```

Second, the Docker images used to create a secure sandbox need to be built before CodeBot commands are executed. To do so, first build the codebox image by running `bash sandbox/codebox/build.sh` -- this image will take a very long time to build. Once the codebox image is built, build the sandbox image by running `bash sandbox/build.sh`. The codebox image is a base image containing all needed packages and libraries for the included languages. A new sandbox image is created for each piece of code submitted using the codebox base image.

To start CodeBot, then run `python3 main.py` on a Linux platform.

## Use

Once CodeBot is connected to a server, use `>help` to get more information on executing code. In brief, code is submited to the bot using code blocks in Discord; the code contained within the block is run and the language is declared via the language listed for the code block's highlighting syntax.
