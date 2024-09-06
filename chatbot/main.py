from activities.quiz.quizz import Quizz
from activities.activity import Activity
from twitchio.ext import commands, routines
import random
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from llm_model import LLM_Model
from datas.prompts import LLM_PROMPTS,ANSWER_TEMPLATE,ANNOUNCEMENT_MSG

URL = 'http://localhost:5000'

def get_random_entry(list):
        index = random.randint(0,len(list)-1)
        return list[index]

def get_minutes(a,b):
        c = a-b
        return c / 120

def post_process(text):
        print(text)
        while(len(text) > 500):
            sentences = text.split('.')
            text = ""
            for i in range(len(sentences)-2):
                text = text + sentences[i] + '.'
                
        return text

def format(str,params):
     return str.format(**params)

class Bot(commands.Bot):
    def __init__(self):
        load_dotenv()
        uri = os.getenv("MONGO_URL")
        self.client : MongoClient = MongoClient(uri)
        database = self.client.get_database(os.getenv("DB"))
        self.users = database.get_collection("user")
        self.alerts_on = bool(os.getenv("ALERTS_ON") == "True")
        self.model = LLM_Model(os.getenv("LLM_PATH"))
        self.channel = None
        self.current_activity: Activity = None

        super().__init__(token= os.getenv("TOKEN"),
            client_id=os.getenv("CLIENT_ID"),
            nick="Reffyatron",
            prefix="!",
            initial_channels=[os.getenv("INITIAL_CHANNEL")])


    def generate(self,prompt,params,is_generate=True):
        result = ""
        context = prompt["context"]
        text = prompt["text"]
        max_new_tokens = prompt["max_new_tokens"]

        context = format(context,params)
        text = format(text,params)
        if is_generate:
            result = self.model.differ(text=text, max_new_tokens=max_new_tokens)
        else:
            result = self.model.complete(text=text, max_new_tokens=max_new_tokens)
        return post_process(result)

    async def event_message(self, message):
        if message.echo:
             return
        
        if not(self.current_activity == None):
             await self.current_activity.on_message(message)
             if self.current_activity.is_finished(): self.current_activity = None
             
        await self.handle_commands(message)

    async def event_ready(self):
        self.channel = super().get_channel(os.getenv("INITIAL_CHANNEL"))
        self.announcement.start()
        
    @routines.routine(seconds=900, wait_first=True)
    async def announcement(self):
            if(len(self.channel.chatters) > 0 ):
                msg = self.get_random_entry(ANNOUNCEMENT_MSG.MSGS)
                await self.channel.send(msg)

    @commands.command()
    async def start_quiz(self,ctx):
        if self.current_activity:
             await ctx.reply("Sorry, another activity is already in progress")
             return
        
        self.current_activity = Quizz(self.channel)
        await ctx.reply("starting quiz")
        await self.current_activity.start()

    @commands.command()
    async def namelore(self,ctx):
        await ctx.reply("Laisse moi un instant pour trouver l'inspiration.")
        answer = self.generate(LLM_PROMPTS.NAMELORE,{"user" : ctx.author.name, "theme" : get_random_entry(LLM_PROMPTS.NAMELORE.get('themes'))},False)
        await ctx.reply(answer)

    @commands.command()
    async def whyisuck(self,ctx):
        await ctx.reply("L'analyse de ton gameplay est en cours, sois patient")
        answer = self.generate(LLM_PROMPTS.WHYISUCK,{"user" : ctx.author.name, "theme" : get_random_entry(LLM_PROMPTS.WHYISUCK.get("themes"))})
        await ctx.reply(answer)


    @commands.command()
    async def pintefame(self,ctx):
        aggregation = [{ '$sort': { 'commands.pinte.used': -1 } },{'$limit' : 10}]

        leaderboard = self.users.aggregate(aggregation)
        output = ""
        index = 1

        for user in leaderboard:
            output += " " + str(index) + ". " + user["name"] + ": " + str(user["commands"]["pinte"]["used"]) + " pinte(s) |"
            index = index + 1

        output = output[:-1]
        
        
        await ctx.reply(output)

    @commands.command()
    async def namepoetry(self, ctx):
        await ctx.reply("Je génère ton poème, sois patient")
        answer = self.generate(LLM_PROMPTS.NAMEPOETRY,{"user" : ctx.author.name, "forme" : get_random_entry(LLM_PROMPTS.NAMEPOETRY.get("forme")),
                                               "theme" : get_random_entry(LLM_PROMPTS.NAMEPOETRY.get("themes")) })
        await ctx.reply(answer)

    @commands.command()
    async def turbopinte(self,ctx):
        search_query = {"$or" : [{"name" : ctx.author.name},{"id": ctx.author.id}]}
        boost = random.randint(5,20)
        author = self.users.find_one(search_query)
        new_rate = 0
        used = 1
        if not author == None:
            data = author["commands"]["pinte"]
            new_rate = data["rate"] * (0.95**get_minutes(time.time(),data["last_drank"])) + boost
            used = data["used"]+1
            self.users.update_one(search_query, {'$set' : {"name" : ctx.author.name, "id" : ctx.author.id, 'commands' : { 'pinte' : { 'used' : used, 'rate' : new_rate, 'last_drank' : time.time()}}}})
        else:
            new_rate = boost
            self.users.insert_one({"name" : ctx.author.name, "id" : ctx.author.id, "commands" : { "pinte" : {"used" : 1, "rate" : new_rate, "last_drank" : time.time()}}})
    
        if self.alerts_on:
            requests.post(URL+"/put-alert", json={'alert' : 'pinte'})

        params = {"user" : ctx.author.name, "rate" : round(new_rate), "number" : used}
        answer = ANSWER_TEMPLATE.PINTE.format(**params)
        await ctx.reply(answer)
    
if __name__ == '__main__':
    bot = Bot()
    bot.run()
   # client.close()