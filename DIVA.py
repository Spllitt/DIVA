import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp


def runBot():

    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")

    canal_midia_ID = 1426369028825415712
    canal_mid_ID = 1426650658903166978

    handler = logging.FileHandler(filename="discord.log",encoding="utf-8",mode="w")

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="d!",intents=intents)

    yt_dl_options = {"format": "bestaudio/best"}

    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {"options": "-vn"}

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} merda")

    @bot.event
    async def on_message(message):

        if message.author.bot:
            return
        
        # Apaga mensagem nos canais

        if message.channel.id in (canal_midia_ID, canal_mid_ID):

            if not (message.attachments or message.embeds):
                await message.delete()
                return

        # Música
        
        if message.content.startswith("d!p"):

            argumentos = message.content.split()

            if message.author.voice is None:
                await message.channel.send("Você precisa estar em um canal de voz." )
                return

            voice_channel = message.author.voice.channel

            voice_client = message.guild.voice_client

            try:

                if voice_client is None:
                    voice_client = await voice_channel.connect()

                elif voice_client.channel != voice_channel:
                    await voice_client.move_to(voice_channel)

            except Exception as e:

                print("Erro ao conectar:")
                print(type(e))
                print(e)

                await message.channel.send(f"Erro ao conectar ao canal de voz:\n{e}")
                return

            url = argumentos[1]

            try:
                loop = asyncio.get_running_loop()

                data = await loop.run_in_executor(None,lambda: ytdl.extract_info(url,download=False))

                if "url" not in data:

                    await message.channel.send("Não foi possível obter o áudio.")
                    return

                player = discord.FFmpegPCMAudio(executable=r"C:\ffmpeg\ffmpeg.exe", source=data["url"], **ffmpeg_options)

                if voice_client.is_playing():
                    voice_client.stop()

                voice_client.play(player)

                await message.channel.send(f"Tocando:\n{data['title']}")

            except Exception as e:

                print("Erro ao reproduzir:")
                print(type(e))
                print(e)

                await message.channel.send(f"Erro ao reproduzir a música:\n{e}")

        await bot.process_commands(message)

    bot.run(token,log_handler=handler,log_level=logging.DEBUG)