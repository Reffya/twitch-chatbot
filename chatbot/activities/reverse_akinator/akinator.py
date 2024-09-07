from activities.activity import Activity
import json
import os
import random

from llm.llm_model import differ

CONTEXT_TEMPLATE = "Tu joues à un jeu consistant à deviner à quel personnage tu penses. Tu penses à {personnage}, En voici une description: {description}. Les autres joueurs te posent des questions pour essayer de savoir à quel personnage tu penses. Les autres joueurs ont le droit de poser des questions, réponds par l'affirmatif ou le négatif à chaque question. Si tu ne connais pas la réponse ou que la question ne se répond par par oui ou non, dis que tu ne sais pas. Ne donne jamais le nom du personnage dans une réponse"

def format(str,params):
     return str.format(**params)

def get_random_entry(list):
        index = random.randint(0,len(list)-1)
        return list[index]

class Reverse_Akinator(Activity):

    def __init__(self, channel):
        

        self.channel = channel
        self.personnage = ""
        self.description = ""
        self.ended = False

    async def start(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'personnages.json'), 'r') as file:
            data = json.load(file)

            personnage = get_random_entry(data)
            self.personnage = personnage['nom']
            self.description = personnage['description']

        await self.channel.send("Je suis prêt ! NB: Cette activité est encore en développement, des fois je peux dire des bêtises !")


    async def on_message(self,message):
        if message.content.startswith('!ask'):
            question = message.content.replace('!ask','')
            result = differ(text=question,max_new_tokens=999,context=format(CONTEXT_TEMPLATE,{"personnage" : self.personnage, "description" : self.description }))
            await self.channel.send(result)
        elif self.personnage.casefold() in message.content.casefold():
             await self.end(message.author.display_name)



    async def end(self, winner):
        await self.channel.send("Félications " + winner + " Tu as toruvé à qui je pensais")
        self.ended = True

    def is_finished(self):
        return self.ended

    async def kill(self):
         await self.channel.send("L'activité est annulée bye bye")
