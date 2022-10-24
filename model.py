import random
import string

suits = ['♡', '♤', '♢', '♧']
values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


class Card:
    def __init__(self, suit, value):
        self.__suit: string = suit
        self.__value = value


class Deck:
    def __init__(self):
        self.__cards: list[Card] = []
        for suit in suits:
            for value in values:
                self.__cards.append(Card(suit, value))

        random.shuffle(self.__cards)

