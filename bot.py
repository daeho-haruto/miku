import discord
import asyncio
import random
import urllib.parse
import urllib
from discord.utils import get
from discord.ext import commands


token = "Nzc4OTY5NTA1NDAxMjc0NDA4.X7Zt4g.fuqN1XabWLY87jmCEs9TXpCHHuE"
client = discord.Client()
# client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print("봇 준비 완료!")
    print(client.user)
    print("---------------")

@client.event
    


client.run(token)