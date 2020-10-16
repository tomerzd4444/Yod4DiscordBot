import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="please ")
load_dotenv(dotenv_path="token.env")
token = os.getenv('token')
homeworkDict = {}
print(token)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="the zoom lesson"))

def printDict(d: dict):
    toReturn = ""
    for key, value in d.items():
        toReturn += f"{key}: {', '.join(value)} \n"
    return toReturn

def addWork(lessonName: str, work: str):
    if not homeworkDict.get(lessonName):
        homeworkDict[lessonName] = []
    homeworkDict[lessonName].append(work)

@bot.command()
async def homework(ctx: discord.ext.commands.context.Context):
    print(type(ctx))
    await ctx.send("working")


@bot.command()
async def setHomework(ctx: discord.ext.commands.context.Context, lessonName: str, *work: str):
    print(work)
    work = ' '.join(work)
    print(work)
    addWork(lessonName, work)

    await ctx.send(f"set the homework of the lesson {lessonName}!")
    # await ctx.send(printDict(homeworkDict))


@bot.command()
async def getHomework(ctx: discord.ext.commands.context.Context):
    await ctx.send(printDict(homeworkDict))

bot.run(token)
