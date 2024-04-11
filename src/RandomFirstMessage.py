import random


class RandomFirstMessage:
    """
    Cette classe permet d'afficher un message aléatoire en console lorsque l'utilisateur lance un niveau.
    """

    MESSAGES = ["Bonne chance !",
                "Niveau initialisé avec succès vous pouvez jouer.",
                "A vous de jouer !",
                "Prenez le temps qu'il faut pour trouver la solution.",
                "Cliquez sur le bouton \"Aide\" si vous avez des difficultés",
                "Faite preuve de logique et créativité pour venir à bout de ce niveau.",
                "Montrez à ce niveau ce que vous savez faire !",
                "Allez, au travail !",
                "Vous allez y arriver !",
                "Vous pouvez jouer !",
                "Recommencez le niveau autant de fois que nécessaire !",
                "Il y a souvent plusieurs façon de réussir un niveau...",
                "Chaque niveau résolu est vrai victoire.",
                "Pensez vous être capable de finir ce niveau ?",
                "Chaque erreur est une leçon.",
                "Accomplissez votre mission !",
                "Il existe peut-être une manière détournée pour finir chaque niveau.",
                "Aucun niveau n'est impossible à finir (c'est promis).",
                "Certains niveaux peuvent êtres plus dur que d'autres, il ne faut pas perdre patience.",
                "Montrez de quoi vous êtes capable !",
                "Chacun(e) raisonne à sa manière, montrez ce que vous pouvez faire.",
                "Essayez de faire quelque chose.",
                "Prenez votre temps.",
                "Faites de votre mieux.",
                "Résolvez ce problème.",
                "Terminez ce niveau en respectant l'énoncé (ou pas si vous êtes assez malin).",
                "Soyez malin !",
                "Lancez-vous !",
                "Faites preuve de persévérance !",
                "Allez y !",
                "Apprenez pas à pas.",
                "N'abandonnez jamais !",
                "Vous pouvez exécuter autant de programmes que vous le souhaitez.",
                "Parfois, la réponse est plus simple qu'elle ne paraît",
                "Tentez différentes approches, la solution est à portée de main !",
                "Chaque problème a une solution. À vous de la trouver !",
                "Plusieurs raisonnements sont possibles.",
                ">> Ici s'afficherons les erreurs que vous faites <<",
                ]

    @staticmethod
    def generate():
        """
        :return: Un message aléatoire présent dans la liste MESSAGE.
        """
        assert (len(RandomFirstMessage.MESSAGES) > 0)
        return RandomFirstMessage.MESSAGES[random.randrange(len(RandomFirstMessage.MESSAGES))]
