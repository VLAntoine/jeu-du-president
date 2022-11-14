from json import detect_encoding
import random
from select import select
import string
from constant import VALUES, SUITS, NAMES


class Card:
    def __init__(self, value: string, suit: string):
        self.__suit: string = suit
        self.__value: string = value

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit

    # compare values
    def __eq__(self, other) -> bool:
        return VALUES.index(self.__value) == VALUES.index(other.value)

    def __lt__(self, other) -> bool:
        return VALUES.index(self.__value) < VALUES.index(other.value)

    def __ne__(self, other) -> bool:
        return VALUES.index(self.__value) != VALUES.index(other.value)

    def __gt__(self, other) -> bool:
        return VALUES.index(self.__value) > VALUES.index(other.value)


class Deck:
    def __init__(self):
        self.__cards = []
        for value in VALUES:
            for suit in SUITS:
                self.__cards.append(Card(value, suit))

    @property
    def cards(self):
        return self.__cards

    def __eq__(self, other):
        return self.cards == other.cards

    def shuffle(self):
        random.shuffle(self.__cards)


class Player:
    def __init__(self, name: string = ""):
        self._name: string = random.choice(NAMES) if name == "" else name
        self._hand: list[Card] = []

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    def add_to_hand(self, card: Card):
        self._hand.append(card)

    def remove_from_hand(self, card: Card):
        self._hand.remove(card)

    def has_card(self, card: Card):
        return card in self._hand

    def play(self, cards: list[Card]):
        for card in cards:
            self.remove_from_hand(card)


class Trick:
    def __init__(self):
        self.__cards: list[Card] = []
        # le nombre de cartes demandé pour le pli en cours
        self.__number_of_cards = 0

    def add_cards(self, cards: list[Card]):
        self.__cards.extend(cards)

    @property
    def cards(self):
        return self.__cards

    @property
    def number_of_cards(self):
        return self.__number_of_cards

    @number_of_cards.setter
    def number_of_cards(self, number):
        self.__number_of_cards = number


class AIPlayer(Player):
    def __init__(self, name: string):
        super().__init__(name)

    def play(self, card: Card):
        self._hand.remove(card)


class PresidentGame:
    def __init__(self, players: list[Player] = None, number_of_sets: int = 1):
        self.__players = [Player(), Player(), Player()
                          ] if players is None else players
        self.distribute()
        self.__current_trick: Trick = Trick()
        self.__current_player_index: int = 0
        self.__turns_without_plays: int = 0
        self.__numbuer_of_sets: int = number_of_sets

    @property
    def players(self):
        return self.__players

    @property
    def current_player_index(self):
        return self.__current_player_index

    @current_player_index.setter
    def current_player_index(self, index: int):
        self.__current_player_index = index

    @property
    def turns_without_plays(self):
        return self.__turns_without_plays

    def distribute(self):
        deck = Deck()
        deck.shuffle()
        cards = deck.cards
        number_of_players = len(self.players)
        for index, card in enumerate(cards):
            player = self.players[index % number_of_players]
            player.add_to_hand(card)

    def next_player(self):
        self.__current_player_index = (
            self.__current_player_index + 1) % len(self.__players)

    def skip_turn(self):
        self.__turns_without_plays += 1

    def play(self, cards: list[Card]):
        self.players[self.__current_player_index].play(cards)
        self.__current_trick.add_cards(cards)

    def end_turn(self):
        # Fin d'un tours si un 2 est posé ou que personne n'as joué
        punchline = ['a plié le game', 'vous emmerde tous', 'prouve ça supériorité', 'est le plus fort']

        if self.__turns_without_plays >= list[Player]:
            print("Fin du tour, personne n'as joué...")

            self.__current_trick: Trick = Trick()
            self.__current_player_index: int = 0
            self.__turns_without_plays: int = 0
            self.__numbuer_of_sets - 1

        if list[Card] == "2":
            print(self.players, " ", random.choice(punchline), " avec un 2")

            self.__current_trick: Trick = Trick()
            self.__current_player_index: int = 0
            self.__turns_without_plays: int = 0
            self.__numbuer_of_sets - 1
        pass

    def end_set(self):
        # Fin du set si un seul joueur a des carte ou personne n'a jouer
        # attributiondes roles + increment nb_de_set
        user_without_cards = 0
        for player in self.__players:
            if player.has_card == 0:
                user_without_cards += 1
                print(player.name, " n'a plus de cartes")
        if user_without_cards == player - 1:
            print("fin du set : personne n'a joué")

        pass

    def end_game(self):
        # Nb de sets max atein Affichage des scores
        if self.__numbuer_of_sets == 0:
            print("Partie terminé : plus assé de tours")
        pass
