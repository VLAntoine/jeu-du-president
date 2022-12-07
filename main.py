from model import Player, AIPlayer
from view import CommandLineView

players: list[Player] = [Player(), AIPlayer("Norbert"), AIPlayer("Danielle")]

commandLineView = CommandLineView(players)
