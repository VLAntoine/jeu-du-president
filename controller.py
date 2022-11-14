from model import PresidentGame, Card, Player
import utils
from utils import NotInRulesException, WrongRequestException


class PresidentGameController:

    def __init__(self, players: list[Player] = None, number_of_sets: int = 1):
        self.__game = PresidentGame(players)

    def play(self, request: dict):

        try:
            # teste si la forme de la requête est bonne et si la requête est dans les règles
            utils.check_request(request, self.__game)

            # si request.skip est True, passe la main au joueur suivant
            if request["skip"]:
                self.__game.skip_turn()
            else:
                value = request["cards"]["value"]
                suits = request["cards"]["suits"]
                cards: list[Card] = []

                for suit in suits:
                    cards.append(Card(value, suit))

                # jouer les cartes de la requête
                self.__game.play(cards)
                pass

            self.__game.end_turn()
            self.__game.end_set()
            self.__game.end_game()

        except (NotInRulesException, WrongRequestException) as error:
            raise error
