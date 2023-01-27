from discord import *
from discord.ext import commands
import discord
import os
import asyncio

Client = commands.Bot(command_prefix="/",intents=Intents.default())
Client.remove_command("help")

@Client.event
async def on_ready():
    print(f"Logged in as {Client.user.name}")

    await Client.change_presence(activity=Activity(type=ActivityType.unknown, name=""), status=Status.do_not_disturb)

    try:
        synced = await Client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def LoadModules():
    for file in os.listdir("./Modules"):
        if file.startswith("_"):
            continue
        if file.endswith(".py"):
            await Client.load_extension(f"Modules.{file[:-3]}")
            print(f"Loaded Modules.{file[:-3]}")

print("\nLoading Modules...")
asyncio.run(LoadModules(),debug=None)

with open("Token.txt", "r") as f:
    Client.run(f.read())