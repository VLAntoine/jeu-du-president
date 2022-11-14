from model import PresidentGame, Card


class PresidentGameController:

    def __init__(self):
        self.__game = PresidentGame()

    def play(self, request: dict):
        # TODO: teste si la requête est globalement dans les règles et si la forme est bonne

        # si request.skip est True, passe la main au joueur suivant
        if request["skip"]:
            self.__game.skip_turn()
        else:
            value = request["card"]["value"]
            suits = request["card"]["suit"]
            cards: list[Card] = []

            for suit in suits:
                card = Card(value, suit)

            # TODO teste si les cartes peuvent être jouées dans les règles (au-dessus de la / des précédente(s), bon nombre de cartes, etc.)

            # TODO: jouer la carte de la requête
            pass

        self.__game.end_turn()
        self.__game.end_set()
        self.__game.end_game()
