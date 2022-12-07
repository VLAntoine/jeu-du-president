import random
import string
from constant import VALUES, SUITS, NAMES
from itertools import combinations


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

    def __str__(self):
        return self.__value + self.__suit


class Cards:
    def __init__(self):
        self.__cards = []

    @property
    def cards(self):
        return self.__cards

    def append(self, card: Card):
        self.__cards.append(card)


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


class Trick:
    def __init__(self):
        self.__cards: list[Card] = []
        # le nombre de cartes demandé pour le pli en cours
        self.__number_of_cards = 0
        # le dernier joueur à avoir posé une carte
        self.__last_player_index = -1

    def add_cards(self, cards: list[Card], player_index: int):
        if len(self.__cards) == 0:
            self.__number_of_cards = len(cards)
        self.__cards.extend(cards)
        self.__last_player_index = player_index

    @property
    def cards(self):
        return self.__cards

    @property
    def number_of_cards(self):
        return self.__number_of_cards

    @number_of_cards.setter
    def number_of_cards(self, number):
        self.__number_of_cards = number

    @property
    def last_player_index(self):
        return self.__last_player_index

    def __str__(self):
        cards_str = ""
        for card in self.cards:
            cards_str += f'{card} '
        return f'[Trick\n\tCartes : {cards_str}\n\tNombre de cartes demandées : {self.__number_of_cards}\n]'


class Player:
    def __init__(self, name: string = ""):
        self._name: string = random.choice(NAMES) if name == "" else name
        self._hand: list[Card] = []
        self._role = None

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role: string):
        self._role = role

    def add_to_hand(self, card: Card):
        self._hand.append(card)

    def remove_from_hand(self, card: Card):
        self._hand.remove(card)

    def clear_hand(self):
        self._hand = []

    def has_card(self, card: Card):
        return card in self._hand

    def play(self, cards: list[Card]):
        for card in cards:
            self.remove_from_hand(card)

    def get_cards_allowed(self, trick: Trick):
        trick.cards.sort()
        cards_as_dict = get_cards_as_dict(self._hand)
        cards_allowed = []
        for value, cards in cards_as_dict.items():
            if cards[0] > trick.cards[-1] and \
                    len(cards) >= trick.number_of_cards:
                cards_allowed.extend(cards)
        return cards_allowed

    def __str__(self):
        cards_str = ""
        for card in self.hand:
            cards_str += f'{card} '
        return f'[Joueur {self._name}\n\tCartes : {cards_str}\n\tRôle : {self._role}]'


class AIPlayer(Player):
    def __init__(self, name: string = ''):
        super().__init__(name)

    def random_cards_to_play(self, trick: Trick) -> [Card]:
        cards_allowed = self.get_cards_allowed(trick)
        cards_allowed_dict = get_cards_as_dict(cards_allowed)
        values = list(cards_allowed_dict.keys())
        random_value = random.choice(values)
        cards_combination_allowed = list(combinations(cards_allowed_dict[random_value], trick.number_of_cards))
        # ajoute une liste vide, si elle est retenue, l'ia passe son tour
        cards_combination_allowed.append([])
        return random.choice(cards_combination_allowed)


class PresidentGame:
    def __init__(self, players: list[Player] = None, number_of_sets: int = 1):
        self.__players = [Player(), Player(), Player()
                          ] if players is None else players
        self.distribute()
        self.__current_trick: Trick = Trick()
        self.__current_player_index: int = 0
        self.__turns_without_plays: int = 0
        self.__number_of_sets: int = number_of_sets
        self.__current_set: int = 0
        self.__nb_players_without_card = 0
        self.start_set()

    @property
    def players(self):
        return self.__players

    @property
    def current_trick(self):
        return self.__current_trick

    @property
    def current_player_index(self):
        return self.__current_player_index

    @current_player_index.setter
    def current_player_index(self, index: int):
        self.__current_player_index = index

    @property
    def turns_without_plays(self):
        return self.__turns_without_plays

    def get_current_player(self):
        return self.__players[self.__current_player_index]

    def distribute(self):
        deck = Deck()
        deck.shuffle()
        cards = deck.cards
        number_of_players = len(self.players)
        for index, card in enumerate(cards):
            player = self.players[index % number_of_players]
            player.add_to_hand(card)

    def next_player(self):
        self.__current_player_index = \
            (self.__current_player_index + 1) % len(self.__players)

    def skip_turn(self):
        self.__turns_without_plays += 1

    def play(self, cards: list[Card]):
        self.__turns_without_plays = 0
        current_player = self.players[self.__current_player_index]
        current_player.play(cards)
        self.__current_trick.add_cards(cards, self.__current_player_index)
        if len(current_player.hand) == 0:
            self.__nb_players_without_card += 1
            self.assign_role(current_player)

    def assign_role(self, player: Player):
        nb_players = len(self.__players)
        if self.__nb_players_without_card == 1:
            player.role = "Président"
        elif self.__nb_players_without_card == 2 and nb_players >= 4:
            player.role = "Vice-Président"
        elif self.__nb_players_without_card == nb_players - 1 and nb_players >= 4:
            player.role = "Vice-Trou"
        elif self.__nb_players_without_card == nb_players:
            player.role = "Trou"
        else:
            player.role = "Neutre"

    def is_turn_ended(self):
        self.__current_trick.cards.sort()
        return (self.__turns_without_plays >= len(self.__players)
                or self.__current_trick.cards[-1].value == 2)

    def end_turn(self):
        self.__current_player_index = self.__current_trick.last_player_index
        self.__current_trick = Trick()
        self.__turns_without_plays = 0

    def start_set(self):
        if self.__current_set == 0:
            for index, player in enumerate(self.__players):
                if player.has_card(Card("Q", "♡")):
                    self.__current_player_index = index
        else:
            for index, player in enumerate(self.__players):
                if player.role == "Trou":
                    self.__current_player_index = index

    def is_set_ended(self):
        # Fin du set si un seul joueur a des cartes
        return self.__nb_players_without_card == len(self.__players) - 1

    def end_set(self):
        for index, player in enumerate(self.__players):
            if len(player.hand) != 0:
                player.role = "Trou"
                self.__current_player_index = index
                player.clear_hand()
        self.__current_set += 1

    def is_game_ended(self):
        # Nb de sets max atteint
        return self.__current_set >= self.__number_of_sets

    def end_game(self):
        pass

    def __str__(self):
        players_str = ""
        for player in self.__players:
            players_str += f'{player}\n'
        return f"Joueurs : \n{players_str}" \
               f"\nPli en cours:" \
               f"\n{self.__current_trick}" \
               f"\nTour de {self.__players[self.__current_player_index].name}" \
               f"\nManche {self.__current_set + 1}" \
               f"\nNombre de manches total : {self.__number_of_sets}" \
               f"\nNombre de tours sans cartes jouées : {self.__turns_without_plays}" \
               f"\nNombre de joueurs sans cartes : {self.__nb_players_without_card}"


def get_cards_as_dict(cards: [Card]) -> dict[int, list[Card]]:
    cards_as_dict = {}
    for card in cards:
        cards_of_value = cards_as_dict[card.value]
        cards_as_dict[card.value] = [card] + cards_of_value
    return cards_as_dict
