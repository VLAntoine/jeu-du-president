import random
import string

SUITS = ['♡', '♤', '♢', '♧']
VALUES = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


class Card:
    def __init__(self, value: string, suit: string):
        self.__suit: string = suit
        self.__value: string = value

    @property
    def value(self):
        return self.__value

    def __eq__(self, other):
        return self.__value == other.value


class Deck:
    def __init__(self):
        self.__cards: list[Card] = []
        for value in VALUES:
            for suit in SUITS:
                self.__cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.__cards)


class Player:
    def __init__(self, name: string, cards: list[Card]):
        self._name: string = name
        self._hand: list[Card] = cards

    def add_to_hand(self, card: Card):
        self._hand.append(card)

    def remove_from_hand(self, card: Card):
        self._hand.remove(card)

    def play(self, card: Card):
        pass


class AIPlayer(Player):
    def __init__(self, name: string, cards: list[Card]):
        super().__init__(name, cards)

    def play(self, card: Card):
        self._hand.remove(card)
