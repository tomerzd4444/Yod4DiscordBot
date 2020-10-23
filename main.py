import os
import discord
import mysql.connector
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime


bot = commands.Bot(command_prefix=";")
load_dotenv(dotenv_path="token.env")
token = os.getenv('token')
subjectList = ["Math", "English", "Hebrew", "Biology", "Cinema", "Arabic", "Tanah", "History", "Literature",
               "SocialStudies", "Yigal", "Sport", "CS", "Physics", "Chemistry"]
print(token)
mydb = mysql.connector.connect(
    host="141.226.192.71",
    user="yodadmin",
    password="yoddbadmin",
    database="yod4"
)


@tasks.loop(hours=4)
async def autoDelete():
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM homework WHERE date < DATE(\'" + datetime.now().strftime("%Y-%m-%d") + "\')")
    mydb.commit()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.watching, name="the zoom lesson"))
    autoDelete.start()


@bot.command()
async def subjects(ctx: discord.ext.commands.context.Context):
    await ctx.send(f'subjects: {subjectList}')


@bot.command()
async def homework(ctx: discord.ext.commands.context.Context):
    print(type(ctx))
    await ctx.send("working")


@bot.command
async def sethw(ctx: discord.ext.commands.context.Context, date: str, subject: str, *work: str):
    parsedTime = datetime.strptime(date, "%d-%m-%Y")
    workString = ' '.join(work)
    if subject.lower() not in map(str.lower, subjectList):  # Checking if the subject exists.
        await ctx.send(f"There is no such subject.")
        return
    mycursor = mydb.cursor()
    query = "INSERT INTO homework (work, subject, date) VALUES (%s, %s, %s)"
    val = (workString, subjectList, parsedTime)
    mycursor.execute(query,
                     val)  # Adding the new assignment, it automatically gets indexed by subject and date and by date alone
    mydb.commit()
    await ctx.send(f"Set the homework of the lesson {subject.lower()}!")


@bot.command()
async def gethw(ctx: discord.ext.commands.context.Context):
    for s in subjectList:
        embed = discord.Embed(color=0x1f49ab, title=s)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT work, date FROM homework WHERE subject = \'" + s + "\' ORDER BY date ASC")
        myresult = mycursor.fetchall()
        if mycursor.rowcount > 0:
            embedWork = ""  # The date and work for each result, we add them together so the embed string looks good and side by side
            embedDate = ""
            for x in myresult:  # Adding embed dates and embed works for all results
                embedWork += x[0] + "\n"
                embedDate += x[1].strftime("%d-%m-%Y") + "\n"  # parsing datetime to string
            embed.add_field(name="Work:", value=embedWork, inline=True)
            embed.add_field(name="Date:", value=embedDate, inline=True)
            await ctx.send(embed=embed)


@bot.command()
async def delhw(ctx: discord.ext.commands.context.Context, *work: str):
    workString = ' '.join(work)
    if workString == '':
        await ctx.send("Please provide an assignment to delete.")
        return
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM homework WHERE work = \'" + workString + "\'")
    mydb.commit()
    await ctx.send("Deleted assignment.")


@bot.command()
async def name(ctx: discord.ext.commands.context.Context, *name: str):
    user = ctx.message.author
    try:
        await user.edit(nick=' '.join(name))
        await ctx.send(f'Nickname was changed for {user.mention}')
    except Exception as e:
        await ctx.send(f'I had an error doing that: ' + str(e))


bot.run(token)
