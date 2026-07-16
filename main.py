import asyncio
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import yt_dlp

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
canal_midia_ID= 1426369028825415712
canal_mid_ID= 1426650658903166978


handler = logging.FileHandler(filename= 'discord.log', encoding= 'utf-8', mode= 'w')
intents = discord.Intents.default()
intents.message_content = True

voice_clients = {}
yt_dl_options = yt_dlp.YoutubeDL({'format': 'bestaudio/best'})
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg = {"options" : "-vn"}



bot = commands.Bot(command_prefix = 'd!', intents = intents)

@bot.event
async def on_ready():

    print(f"{bot.user.name} merda")

@bot.event

async def on_message(message):

    if (message.channel.id == canal_midia_ID or canal_mid_ID):

        if message.author.bot:
            return
        
        if not (message.attachments or message.embeds):
            
            await message.delete()

            return
    await bot.process_commands(message)
    
bot.run(token, log_handler= handler, log_level = logging.DEBUG)