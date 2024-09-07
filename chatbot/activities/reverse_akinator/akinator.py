from activities.activity import Activity
import json
import os
import random
import time

from llm.llm_model import differ

CONTEXT_TEMPLATE = "Tu joues à un jeu consistant à deviner à quel personnage tu penses. Tu penses à {personnage}. Les autres joueurs te posent des questions pour essayer de savoir à quel personnage tu penses. Les autres joueurs ont le droit de poser des questions, réponds par l'affirmatif ou le négatif à chaque question. Si tu ne connais pas la réponse ou que la question ne se répond par par oui ou non, dis que tu ne sais pas. Ne donne jamais le nom du personnage dans une réponse"

CHOOSE_CHAR = "Tu joues à un jeu consistant à deviner à quel personnage tu penses. Choisis au hasard le nom d'une figure ou d'un dieu dans la mythologie {mythologie}. Choisis si possible une divinité ou une figure liée au thème suivant: {theme}. Réponds uniquement avec le nom du personnage, si possible dans sa version la plus connue avec le moins de mots possibles"
MYTHOLOGIES = ['grecque','romaine','egyptienne','nordique','celte','arthurienne','chinoise','hindoue','japonaise','yoruba','maya', 'polynésienne']
THEMES = ["La mort", "l'amour", "le tonerre", "l'eau" , "la lune", "le soleil", "le feu", "la guerre", "le vent", "héros (pas un dieu mais un humain exceptionnel)", "L'agriculture", "le chant", "la fête", "l'art" ]

GENERATE_DESCRIPTION = "Ecris une description du personnage {personnage} en Français."


READY_NON_RANDOM = "Je suis prêt, le jeu est lancé en mode non random, j'ai choisi mon personnage parmi une liste prédéfinie ! NB: cette fonctionnalité est encore en développement, je peux dire des bêtises !"

READY_RANDOM = "Je suis prêt, le jeu est lancé en mode random. J'ai choisi une figure mythologique qui n'est pas forcément dans smite. NB: Cette feature est extrêmement expérimentale"

WIN_USER = "Bravo {user}, tu as trouvé à qui je pensais !"
WIN_BOT = "GG à moi, le personnage auquel je pensais était: {personnage}" 


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

    async def start(self, random_mode):
        if not(random_mode):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'personnages.json'), 'r') as file:
                data = json.load(file)
                personnage = get_random_entry(data)
                self.personnage = personnage['nom']

            await self.channel.send(READY_NON_RANDOM)
        else:
            prompt = format(CHOOSE_CHAR,{"mythologie" : get_random_entry(MYTHOLOGIES), "theme" : get_random_entry(THEMES) })
            perso = differ(text=prompt,temperature=1,seed=int(time.time()),top_k=1000)
            self.personnage=perso
            await self.channel.send(READY_RANDOM)


        



    async def on_message(self,message):
        if message.content.startswith('!ask'):
            question = message.content.replace('!ask','')
            result = differ(text=question,max_new_tokens=999,context=format(CONTEXT_TEMPLATE,{"personnage" : self.personnage}))
            await self.channel.send(result)
        elif message.content.startswith('!f6'):
             await self.end("superfatbot2")
        elif self.personnage.casefold() in message.content.casefold():
             await self.end(message.author.display_name)



    async def end(self, winner):
        if not(winner == "superfatbot2"):
             await self.channel.send(format(WIN_USER,{"user" : winner}))
        else:
             await self.channel.send(format(WIN_BOT,{"personnage" : self.personnage}))
        self.ended = True

    def is_finished(self):
        return self.ended

    async def kill(self):
         await self.channel.send("L'activité est terminée sans gagnant")
