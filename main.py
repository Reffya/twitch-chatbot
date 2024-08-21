from twitchio.ext import commands
import random
import time
import os


def get_minutes(a,b):
    c = a-b
    return c / 120

alcool_rates = {}

bot = commands.Bot(
    token= os.environ["TOKEN"],
    client_id=os.environ["CLIENT_ID"],
    nick="Reffyatron",
    prefix="!",
    initial_channels=['superfatyoh2']
)


@bot.event
async def event_message(ctx):
    print(ctx.author.name)
    print(ctx.content)


@bot.command(name='turbopinte')
async def test_command(ctx):
    boost = random.randint(5,20)
    res = [boost,time.time()]
    author = ctx.author.name
    if author in alcool_rates:
        data = alcool_rates.get(author)
        new_rate = data[0] * (0.9**get_minutes(time.time(),data[1])) + boost
        res = [new_rate, time.time()]
    alcool_rates.update({author : res})
    print(author)
    print("tu es bourré à " + str(res) +"%")
    await ctx.reply("tu es bourré à " + str(int(res[0])) +"%")

    
        
    

if __name__ == '__main__':
    bot.run()