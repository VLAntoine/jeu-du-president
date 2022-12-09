from model import PresidentGame, Card, Player, AIPlayer, Cards
import utils
from exception import NotInRulesException, WrongRequestException


class PresidentGameController:
    """
    La classe controller qui reçoit la requête de l'utilisateur sous forme d'un dictionnaire, appelle les composantes du
    modèle en conséquence et retourne les informations nécessaires à l'affichage graphique à la vue (un DTO).
    """

    def __init__(self, players: list[Player] = None, number_of_sets: int = 1):
        """
        Le constructeur de la classe PresidentGameController.
        """
        self.__game = PresidentGame(players, number_of_sets)
        # effectue les premiers tours des intelligences artificielles si c'est à elles de jouer
        self.ai_turn()

    def get_game_dto(self):
        """
        Retourne un Data Transfer Object sous forme d'un dictionnaire, contenant l'information nécessaire et suffisante
        à l'affichage
        """
        game = self.__game
        players = game.players
        current_trick = game.current_trick
        trick_last_player_index = game.current_trick.last_player_index
        current_player = game.get_current_player()
        game_dto = {
            "current_player_index": game.current_player_index,
            "current_player": {
                "name": current_player.name,
                "hand": [str(card) for card in current_player.hand],
                "role": current_player.role
            },
            "turns_without_play": game.turns_without_plays,
            "current_set": game.current_set + 1,
            "is_trade": game.is_trade,
            "current_trick": {
                "cards": [str(card) for card in current_trick.cards],
                "number_of_cards": current_trick.number_of_cards,
                "last_player": players[trick_last_player_index].name if trick_last_player_index >= 0 else None
            },
            "players": [],
            "is_ended": game.is_game_ended()
        }
        for player in players:
            game_dto["players"].append(
                {
                    "name": player.name,
                    "hand": [str(card) for card in player.hand],
                    "role": player.role
                })
        return game_dto

    def process(self, request: dict = None):
        """
        Traite la requête envoyée par l'utilisateur et met à jour le modèle (le jeu).
        """
        try:
            # teste si la forme de la requête est bonne
            utils.check_request(request)

            # si request.skip est True, passe le tour du joueur
            if request["skip"]:
                # teste si le joueur a le droit de passer, d'après les règles
                utils.check_skip(self.__game)
                self.__game.skip_turn()
            # sinon,
            else:
                # génère les cartes de la requête
                cards = Cards()
                for card_str in request["cards"]:
                    cards.append(Card(card_str[0], card_str[1]))

                # si le jeu en est à la phase d'échange des cartes
                if self.__game.is_trade:
                    # teste si l'échange est dans les règles
                    utils.check_trade(self.__game, cards)
                    # met les cartes à l'échange
                    self.__game.add_cards_to_trade(cards)
                    # met éventuellement fin à l'échange
                    if self.__game.is_trade_over():
                        self.__game.trade_cards()

                # jouer les cartes de la requête
                else:
                    # teste si le coup est valable
                    utils.check_play(self.__game, cards)
                    self.__game.play(Cards(cards))

            # passe la main au joueur suivant
            self.__game.next_player()

            # effectue les tours des IA.
            self.ai_turn()

        except (NotInRulesException, WrongRequestException) as error:
            raise error

    def ai_turn(self):
        """
        Effectue le tour de jeu des différentes IA consécutives.
        """
        # tant que le joueur courant est une intelligence artificielle, joue
        while isinstance(self.__game.get_current_player(), AIPlayer):
            # si le jeu est en phase d'échange, l'ia met des cartes à l'échange puis teste la fin des échanges
            if self.__game.is_trade:
                self.ai_trade()
                if self.__game.is_trade_over():
                    self.__game.trade_cards()
            # sinon l'ia joue des cartes ou passe son tour
            else:
                self.ai_play()
                if self.__game.is_turn_ended():
                    self.end_turn()
            # passe la main au joueur suivant
            self.__game.next_player()

    def ai_play(self):
        """
        L'IA joue une carte ou passe son tour.
        """
        # choisit une liste de cartes au hasard parmi les cartes que l'IA est autorisée à jouer.
        cards_to_play = self.__game.get_current_player().random_cards_to_play(self.__game.current_trick)
        # s'il n'y a pas de carte dans la liste de cartes, passe son tour.
        if len(cards_to_play) == 0:
            self.__game.skip_turn()
        # sinon, joue les cartes de la liste
        else:
            self.__game.play(cards_to_play)

    def ai_trade(self):
        """
        L'IA choisit les cartes qu'elle met à l'échange.
        """
        # choisit au hasard des cartes parmi celles que l'IA peut échanger
        cards_to_trade = self.__game.get_current_player().random_cards_to_trade()
        self.__game.add_cards_to_trade(cards_to_trade)

    def end_turn(self):
        """
        Met à jour les infos de fin de tour et, éventuellement de fin de manche, voire de fin de partie.
        """
        self.__game.end_turn()
        if self.__game.is_set_ended():
            self.__game.end_set()
            if self.__game.is_game_ended():
                self.__game.end_game()
            else:
                self.__game.start_set()
