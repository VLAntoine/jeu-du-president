from model import Player, AIPlayer
from view import CommandLineView

players: list[Player] = [AIPlayer("Benoît"), AIPlayer("Norbert"), AIPlayer("Danielle")]

commandLineView = CommandLineView(players)
