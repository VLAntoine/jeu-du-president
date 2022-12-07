from controller import PresidentGameController
from model import Player


class CommandLineView:
    def __init__(self, players: list[Player], number_of_sets: int = 1):
        self.__controller = PresidentGameController(players, number_of_sets)
        print(self.__controller.game)


