import os
import discord
import mysql.connector
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from datetime import datetime

bot = commands.Bot(command_prefix="hw ")
load_dotenv(dotenv_path="token.env")
token = os.getenv('token')
homeworkDict = {}
subjects = ["Math", "English", "Hebrew", "Biology", "Cinema", "Arabic", "Tanah", "History", "Literature", "SocialStudies", "Yigal", "Sport", "CS", "Physics", "Chemistry"]
print(token)
mydb = mysql.connector.connect(
    host="192.168.1.137",
    user="yodadmin",
    password="yoddbadmin",
    database="yod4"
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="the zoom lesson"))

@bot.command()
async def getSubjects(ctx: discord.ext.commands.contect.Context):
    await ctx.send(f'subjects: {subjects'})
    
@bot.command()
async def homework(ctx: discord.ext.commands.context.Context):
    print(type(ctx))
    await ctx.send("working")

@bot.command
async def sethw(ctx: discord.ext.commands.context.Context, date:str, subject: str, *work: str):
    parsedTime = datetime.strptime(date, "%d-%m-%Y")
    workString = ' '.join(work)
    if subject.lower() not in map(str.lower, subjects): #Checking if the subject exists.
        await ctx.send(f"There is no such subject.")
        return
    mycursor = mydb.cursor()
    query = "INSERT INTO homework (work, subject, date) VALUES (%s, %s, %s)"
    val = (workString, subject, parsedTime)
    mycursor.execute(query, val) #Adding the new assignment, it automatically gets indexed by subject and date and by date alone
    mydb.commit()
    await ctx.send(f"Set the homework of the lesson {subject.lower()}!")


@bot.command()
async def gethw(ctx: discord.ext.commands.context.Context):
    for s in subjects:
        embed = discord.Embed(color=0x1f49ab, title=s)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT work, date FROM homework WHERE subject = \'"+s+"\' ORDER BY date ASC")
        myresult = mycursor.fetchall()
        if(mycursor.rowcount > 0):
            embedWork = "" #The date and work for each result, we add them together so the embed string looks good and side by side
            embedDate = ""
            for x in myresult: #Adding embed dates and embed works for all results
                embedWork += x[0] + "\n"
                embedDate += x[1].strftime("%d-%m-%Y") + "\n" #parsing datetime to string
            embed.add_field(name="Work:", value=embedWork, inline=True)
            embed.add_field(name="Date:", value=embedDate, inline=True)
            await ctx.send(embed=embed)

bot.run(token)
