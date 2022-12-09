from controller import PresidentGameController
from exception import NotInRulesException, WrongRequestException
from model import Player


class CommandLineView:
    """
    L'affichage en ligne de commande du jeu du Président.
    Gère les interactions avec l'utilisateur et transmet les infos qu'il fournit au controller.
    """

    def __init__(self, players: list[Player], number_of_sets: int = 1):
        """
        Le constructeur de la classe CommandLineView.
        Initialise le jeu et déroule toutes les interactions avec l'utilisateur.
        """

        self.__controller = PresidentGameController(players, number_of_sets)
        self.__number_of_sets = number_of_sets
        self.__error = ""
        self.__request = {}

        game = self.__controller.get_game_dto()

        # tant que le jeu n'est pas fini,
        while not game["is_ended"]:
            self.print_game(game)

            player = game["current_player"]
            cards_to_chose = ""
            for index, card in enumerate(player["hand"]):
                cards_to_chose += f"{index}- {card}   "
            cards_to_chose += "\n"

            self.__request = {}
            # initialise l'erreur à 'start' pour rentrer dans la boucle suivante
            self.__error = "start"

            #  tant qu'il y a des erreurs de la part de l'utilisateur
            while self.__error != "":
                # si le jeu est en phase de jeu et non d'échange
                if not game["is_trade"]:

                    # demande à l'utilisateur s'il veut passer
                    choice_skip = "-1"
                    while int(choice_skip) not in [1, 2]:
                        print(f"{player['name']}, voulez-vous passer ? 1- oui    2- non")
                        choice_skip = input()

                    # si l'utilisateur passe, complète la requête
                    if int(choice_skip) == 1:
                        self.__request = {"skip": True}

                    # sinon,
                    else:
                        choice_another_card = "1"
                        self.__request = {"skip": False, "cards": []}

                        # enregistre dans la requête les cartes qu'il veut jouer
                        while int(choice_another_card) == 1:
                            message = f"{player['name']}, quelle carte voulez-vous jouer ?"
                            self.chose_card(message, player, cards_to_chose)
                            message = f"{player['name']}, voulez-vous jouer une autre carte ? 1- oui  2- non"
                            choice_another_card = self.another_card(message)

                # si le jeu est en phase d'échange
                else:
                    self.__request = {"skip": False, "cards": []}
                    choice_another_card = "1"

                    # enregistre dans la requête les cartes que l'utilisateur veut échanger
                    while int(choice_another_card) == 1:
                        message = f"{player['name']}, quelle carte voulez-vous échanger ?"
                        self.chose_card(message, player, cards_to_chose)
                        message = f"{player['name']}, voulez-vous échanger une autre carte ? 1- oui  2- non"
                        choice_another_card = self.another_card(message)

                # envoie la requête à l'utilisateur
                try:
                    self.__controller.process(self.__request)
                    self.__error = ""
                # récupère une erreur (une faute de jeu ou une requête incorrecte) s'il y en a une, et l'affiche
                except (NotInRulesException, WrongRequestException) as error:
                    self.__error = str(error)
                    print(f"Erreur : {self.__error}")

    def chose_card(self, message, player, cards_to_chose):
        """
        Gère les interactions avec l'utilisateur impliquant un choix de cartes
        """
        choice_card = "-1"
        hand = player["hand"]
        # tant que l'indice de la carte choisie n'est pas un des indices des cartes de l'utilisateur, demande à
        # l'utilisateur quelle carte (indice) il veut jouer.
        while int(choice_card) not in range(len(hand)):
            print(message)
            print(cards_to_chose)
            choice_card = input()
        self.__request["cards"].append(player["hand"][int(choice_card)])

    def another_card(self, message):
        """
        Gère les interactions avec l'utilisateur lui demandant s'il veut ajouter une autre carte
        """
        choice_another_card = "0"
        while int(choice_another_card) not in [1, 2]:
            print(message)
            choice_another_card = input()
        return choice_another_card

    def print_game(self, game):
        """
        Affiche l'état actuel du jeu
        """
        game_str = "Manche " + str(game["current_set"]) + "/" + str(self.__number_of_sets) + "\n"
        for index, player in enumerate(game["players"]):
            game_str += player["name"]
            if index == game["current_player_index"]:
                game_str += '*'
            if player["role"] is not None:
                game_str += " - " + player["role"]
            game_str += " : "
            for card in player["hand"]:
                game_str += card + " "
            game_str += "\n"

        game_str += "\n"

        if game["current_trick"]["number_of_cards"] != 0:
            game_str += "Pli en cours (" + game["current_trick"]["number_of_cards"] + ") : "
            for card in game["current_trick"]["cards"]:
                game_str += card + " "
            game_str += " - " + game["current_trick"]["last_player"] + "\n"

        print(game_str)
