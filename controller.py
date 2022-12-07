from model import PresidentGame, Card, Player, AIPlayer
import utils
from utils import NotInRulesException, WrongRequestException


class PresidentGameController:

    def __init__(self, players: list[Player] = None, number_of_sets: int = 1):
        self.__game = PresidentGame(players)

    @property
    def game(self):
        return self.__game

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

            self.__game.next_player()

            while isinstance(self.__game.get_current_player(), AIPlayer) and not self.__game.is_turn_ended():
                self.ai_player_play(self.__game.get_current_player())
                self.__game.next_player()

        except (NotInRulesException, WrongRequestException) as error:
            raise error

    def ai_player_play(self, ai_player: AIPlayer):
        cards_to_play = ai_player.random_cards_to_play(self.__game.current_trick)
        if len(cards_to_play) == 0:
            self.__game.skip_turn()
        else:
            self.__game.play(cards_to_play)

    def end_turn(self):
        self.__game.end_turn()
        if self.__game.is_set_ended():
            self.__game.end_set()
            if self.__game.is_game_ended():
                self.__game.end_game()
