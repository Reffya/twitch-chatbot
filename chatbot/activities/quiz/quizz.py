from activities.activity import Activity
import importlib.resources
import os
import json
import random
import time

from datas.prompts import QUIZ_TEMAPLATES

def get_random_entry(list):
        index = random.randint(0,len(list)-1)
        return list[index]

def format(str,params):
     return str.format(**params)


class Quizz(Activity):

    def __init__(self,channel):
        self.channel = channel
        self.scores = {}
        self.crt_question  = []
        self.ended = False
        self.questions = []
        self.template = "{question}"

    async def start(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'questions.json'), 'r') as file:
            data = json.load(file)

            # choosing quiz
            quiz = get_random_entry(data)

        await self.send(format(QUIZ_TEMAPLATES.CHOSEN, {"subject" : quiz["name"]}))
        self.questions = quiz["questions"]
        self.template = quiz["template"]

        await self.ask_question()

    async def send(self,msg,skip_delay=False):
            if not(skip_delay):
                time.sleep(2)
            await self.channel.send(msg)

    async def ask_question(self):

        if(len(self.questions) == 0):
            await self.end("no one")
            return

        question = get_random_entry(self.questions)
        self.questions.remove(question)


        self.crt_question = question
        await self.send(format(self.template,{ "question" : question["question"]}))

    async def on_message(self, message):
        if(not(message.content.casefold() == self.crt_question["answer"].casefold())):
            return
         
        author = message.author.display_name
        crt_score = 0
        if(self.scores.get(author)):
            crt_score = self.scores.get(author)
        crt_score = crt_score + 1
        self.scores.update({author : crt_score})
        if(crt_score == 5):
            await self.end(author)
        else:
            await self.send(format(QUIZ_TEMAPLATES.CORRECT, { "user" : author, "points" : crt_score}),True)
            await self.ask_question()

    async def end(self, winner):
        await self.send(format(QUIZ_TEMAPLATES.END,{"user" : winner}),False)
        self.ended = True

    def is_finished(self):
        return self.ended
    
    async def kill(self):
        await self.send(QUIZ_TEMAPLATES.CANCELLED, False)
        self.ended = True


