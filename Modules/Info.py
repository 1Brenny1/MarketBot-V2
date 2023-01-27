from discord import *
from discord.ext import commands
from discord.ui import Button, View, Select, modal
import discord

import Posts

class Info(commands.Cog):
    def __init__(self, Client):
        self.Client:commands.Bot
        self.Client = Client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__cog_name__} ready")


    @app_commands.command(name="info",description="View info about the bot")
    @app_commands.describe()
    async def post(self, ctx: discord.Interaction) -> None:
        embed = Embed()
        embed.title = "Info"
        embed.description = "A simple discord bot for the DevPortal discord server\n\n**Made By:** Brenny#8775 @ Brenny.tk"

        ctx.response.send_message()
        

async def setup(Client):
    await Client.add_cog(Info(Client))