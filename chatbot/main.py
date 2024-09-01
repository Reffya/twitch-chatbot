from twitchio.ext import commands, routines
import random
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from llm_model import LLM_Model
from prompts import LLM_PROMPTS,ANSWER_TEMPLATE,ANNOUNCEMENT_MSG

load_dotenv()
uri = os.getenv("MONGO_URL")
print(os.getenv("DB"))
client : MongoClient = MongoClient(uri)
database = client.get_database(os.getenv("DB"))
users = database.get_collection("user")
URL = 'http://localhost:5000'
alerts_on = bool(os.getenv("ALERTS_ON") == "True")
model = LLM_Model(os.getenv("LLM_PATH"))

alcool_rates = {}
load_dotenv()
bot = commands.Bot(
        token= os.getenv("TOKEN"),
        client_id=os.getenv("CLIENT_ID"),
        nick="Reffyatron",
        prefix="!",
        initial_channels=[os.getenv("INITIAL_CHANNEL")]
    )

def get_minutes(a,b):
    c = a-b
    return c / 120

def get_random_entry(list):
    index = random.randint(0,len(list)-1)
    return list[index]

def generate(prompt,params):

    context = prompt["context"]
    text = prompt["text"]
    max_new_tokens = prompt["max_new_tokens"]

    context = context.format(**params)
    text = text.format(**params)

    global last_message
    result = ""
    while result == "" :
        result = model.infer(context=context, text=text, max_new_tokens=max_new_tokens)
    last_message = result
    return result

@routines.routine(seconds=900, wait_first=True)
async def announcement():
        channel = bot.get_channel(os.getenv("INITIAL_CHANNEL"))
        if(len(channel.chatters) > 0 ):
            msg = ANNOUNCEMENT_MSG.MSGS[random.randint(0,len(ANNOUNCEMENT_MSG.MSGS)-1)]
            await channel.send(msg)

@bot.event
async def event_message(message):
    print(message)

@bot.command(name='whyisuck')
async def whyisuck(ctx):
    await ctx.reply("L'analyse de ton gameplay est en cours, sois patient")
    answer = generate(LLM_PROMPTS.WHYISUCK,{"user" : ctx.author.name, "theme" : get_random_entry(LLM_PROMPTS.WHYISUCK.get("themes"))})
    print(answer)
    await ctx.reply(answer)


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

@bot.command(name='namepoetry')
async def namepoetry(ctx):
    await ctx.reply("Je génère ton poème, sois patient")
    answer = generate(LLM_PROMPTS.NAMEPOETRY,{"user" : ctx.author.name, "forme" : get_random_entry(LLM_PROMPTS.NAMEPOETRY.get("forme")),
                                               "theme" : get_random_entry(LLM_PROMPTS.NAMEPOETRY.get("themes")) })
    await ctx.reply(answer)

@bot.command(name='turbopinte')
async def turbopinte(ctx):
    search_query = {"$or" : [{"name" : ctx.author.name},{"id": ctx.author.id}]}
    boost = random.randint(5,20)
    author = users.find_one(search_query)
    new_rate = 0
    used = 1
    if not author == None:
        data = author["commands"]["pinte"]
        new_rate = data["rate"] * (0.95**get_minutes(time.time(),data["last_drank"])) + boost
        used = data["used"]+1
        users.update_one(search_query, {'$set' : {"name" : ctx.author.name, "id" : ctx.author.id, 'commands' : { 'pinte' : { 'used' : used, 'rate' : new_rate, 'last_drank' : time.time()}}}})
    else:
        new_rate = boost
        users.insert_one({"name" : ctx.author.name, "id" : ctx.author.id, "commands" : { "pinte" : {"used" : 1, "rate" : new_rate, "last_drank" : time.time()}}})
   
    if alerts_on:
        requests.post(URL+"/put-alert", json={'alert' : 'pinte'})

    params = {"user" : ctx.author.name, "rate" : round(new_rate), "number" : used}
    answer = ANSWER_TEMPLATE.PINTE.format(**params)
    await ctx.reply(answer)
    
if __name__ == '__main__':
    announcement.start()
    bot.run()
    client.close()