import asyncio
import time
from collections import deque

import discord
from discord.ext import commands
from pytube import YouTube
from discord.ext import tasks
import os

intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

songs = deque()
flag = []

def play_next(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.play(discord.FFmpegPCMAudio(executable="D:\\DiscordBot_\\ffmpeg\\bin\\ffmpeg.exe",
                                                  source="mp.mp3"))
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    flag.append("1")
    await channel.connect()

@tasks.loop(seconds=10)
async def play_songs(ctx, ):
    channel = ctx.message.author.voice.channel
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    if len(flag)==0:
        await connect(ctx)
    server = ctx.message.guild
    voice_channel = server.voice_client
    if not voice_channel.is_playing():
        await getAudio(songs.popleft())
        play_next(ctx)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)




@bot.command()
async def play(ctx, url):
    songs.append(url)
    if play_songs.is_running():
        return
    play_songs.start(ctx)



async def getAudio(url):
    #path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mp.mp3')
    #os.remove(path)
    print(url)
    yt = YouTube(url)
    streams = yt.streams.filter(only_audio=True)
    stream = yt.streams.get_by_itag(251)
    stream.download(filename="mp.mp3")


@bot.command()
async def clear(ctx):
    play_songs.stop()
    songs.clear()
    flag.clear()
    channel = ctx.message.author.voice.channel
    server = ctx.message.guild
    voice_channel = server.voice_client
    await voice_channel.disconnect()
    await ctx.send("bot was cleared")


bot.run('token')
