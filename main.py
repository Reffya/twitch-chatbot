from twitchio.ext import commands
import random
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient

uri = os.getenv("MONGO_URL")
client : MongoClient = MongoClient(uri)
database = client.get_database("twitch_chatbot")
users = database.get_collection("user")


def get_minutes(a,b):
    c = a-b
    return c / 120

alcool_rates = {}
load_dotenv()
bot = commands.Bot(
        token= os.getenv("TOKEN"),
        client_id=os.getenv("CLIENT_ID"),
        nick="Reffyatron",
        prefix="!",
        initial_channels=['superfatyoh2','reffya']
    )


@bot.event
async def event_message(ctx):
    print(ctx.author.name)
    print(ctx.content)

@bot.command(name='pintefame')
async def pintefame(ctx):
    aggregation = [{ '$sort': { 'commands.pinte.used': -1 } },{'$limit' : 10}]

    leaderboard = users.aggregate(aggregation)
    output = ""
    index = 1

    for user in leaderboard:
        output += " " + str(index) + ". " + user["name"] + ": " + str(user["commands"]["pinte"]["used"]) + " pinte(s) |"
        index = index + 1

    output = output[:-1]
    
    
    await ctx.reply(output)

@bot.command(name='turbopinte')
async def turbopinte(ctx):
    search_query = {"$or" : [{"name" : ctx.author.name},{"id": ctx.author.id}]}
    boost = random.randint(5,20)
    author = users.find_one(search_query)
    new_rate = 0
    used = 1
    if not author == None:
        data = author["commands"]["pinte"]
        print(data)
        new_rate = data["rate"] * (0.9**get_minutes(time.time(),data["last_drank"])) + boost
        used = data["used"]+1
        users.update_one(search_query, {'$set' : {"name" : ctx.author.name, "id" : ctx.author.id, 'commands' : { 'pinte' : { 'used' : used, 'rate' : new_rate, 'last_drank' : time.time()}}}})
    else:
        new_rate = boost
        users.insert_one({"name" : ctx.author.name, "id" : ctx.author.id, "commands" : { "pinte" : {"used" : 1, "rate" : new_rate, "last_drank" : time.time()}}})
        
    await ctx.reply("Voilà ton verre, tu es bourré à " + str(int(new_rate)) +"%. C'est déjà la " + str(used) + "e fois que tu bois")
    
if __name__ == '__main__':
    bot.run()
    client.close()