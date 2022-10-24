from json import detect_encoding
import random
from select import select
import string

suits = ['♡', '♤', '♢', '♧']
values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


class Card:
    def __init__(self, suit, value):
        self.__suit: string = suit
        self.__value = value

    # compare values
    def __eq__(self, other) -> bool:
        return self.__value == other.value
    def __lt__(self, other) -> bool:
        return self.__value < other.value
    def __ne__(self, other) -> bool:
        return self.__value != other.value
    def __gt__(self, other) -> bool:
        return self.__value > other.value 

    # Compare suits
    def __eq__(self, other) -> bool:
        return self.__value == other.value
    def __ne__(self, other) -> bool:
        return self.__value != other.value

class Deck:
    def __init__(self):
        self.__cards: list[Card] = []
        for suit in suits:
            for value in values:
                self.__cards.append(Card(suit, value))

        random.shuffle(self.__cards)

class PresidentGame(Player) :
    def __init__(self) -> None:
        return 0

    def distribute_cards():
        
