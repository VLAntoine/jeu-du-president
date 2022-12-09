from model import Player, AIPlayer, Cards, Card
from view import CommandLineView

players: list[Player] = [Player("Benoît"), Player("Norbert"), Player("Danielle")]

commandLineView = CommandLineView(players)
