class LLM_PROMPTS:
    PINTE = {
        "context" : "La commande !turbopinte permet aux utilisateurs de faire semblant de boire une pinte, lorsqu'un utilisateur boit son taux d'alcoolémie augmente",
        "text" : "Indique à {user} qu'après avoir bu la pinte, il est maintenant soul à {rate}%. Sois bref et n'utilise pas plus de deux phrases.",
        "max_new_tokens" : 100
    }
    WHYISUCK = {
        "context" : "La commande !pourquoijesuismauvais permet aux utilisateurs de savoir pourquoi ils sont mauvais sur le jeu 'smite 2'.",
        "text" : "{user} souhaite s'améliorer sur le jeu smite 2. Concentre ton explication sur le sujet suivant: {theme} et fais une explication rapide en une phrase. Génère l'explication en Français. ",
        "themes" : ["mécaniques de jeu", "vision de jeu", "attention à la carte", "connaissance des personnages", "choix des objets", "flexibilité dans les rôles"],
        "max_new_tokens" : 150
    }
    NAMEPOETRY = {
        "context" : "La commande !namepoetry permet de générer un petit poème autour du nom de l'utilisateur",
        "text" : "Ecris un court poème sous la forme d'un {forme} autour du pseudo de {user}, sur le sujet de {theme} Ecris le poème en Français",
        "forme" : ["quatrain","tercet","haïkyu","rap"],
        "themes" : ["la nature","les trains","la mythologie","le seigneur des anneaux","l'amour","le temps", "la boisson", "fantaisie", "le ciel" , "les étoiles", "l'eau", "les rêves", "la musique"],
        "max_new_tokens" : 200
    }


class ANSWER_TEMPLATE:
    PINTE = "Voilà {user}, t'es maintenant bourré à {rate}% ! Et c'est déjà la {number}e fois que tu bois."


class ANNOUNCEMENT_MSG:

    MSGS = [
        "Soif ? enfile toi une !turbopinte",
        "Si tu es mauvais sur smite, essaie la commande !whyisuck et laisse moi te guider !",
        "Avec !namepoetry je peux écrire un petit poème rien que pour toi !",
        "Si tu veux savoir quels sont les objets dispo dans smite 2, j'ai fais une longue vidéo récap sur le sujet, ça se passe ici : https://youtu.be/2xMDcGlRirA",
        "Tu démarres sur Smite 2? Voilà un petit guide pour t'expliquer comment build ton perso et où commencer une game! https://youtu.be/BLInFSD2LXg?si=aP-qp6iGbhlHCwtd",
        "Je vois que votre verre est vide, je vous ressers une pinte? !pinte",
        "Tu passes un bon moment dans la taverne de SuperFatYoh? Alors n'oublie pas de suivre la chaine! C'est gratuit et ça nous aide beaucoup!"
    ]