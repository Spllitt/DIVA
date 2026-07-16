import asyncio
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import yt_dlp

def runBot():    
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    canal_midia_ID= 1426369028825415712
    canal_mid_ID= 1426650658903166978


    handler = logging.FileHandler(filename= 'discord.log', encoding= 'utf-8', mode= 'w')
    intents = discord.Intents.default()
    intents.message_content = True

    #area pra musica
    voice_clients = {}
    yt_dl_options = yt_dlp.YoutubeDL({'format': 'bestaudio/best'})
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {"options" : "-vn"}

    #fim da area pra musica


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

        if message.content.startswith('?play'):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[message.guild.id] = voice_client
            except Exception as e:
                await message.channel.send("Você precisa estar em um canal de voz para usar este comando.")
                return
        
            try:
                url = message.content.split()[1]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

                voice_clients[message.guild.id].play(player)
            except Exception as e:
                print(e)
        

    bot.run(token, log_handler= handler, log_level = logging.DEBUG)