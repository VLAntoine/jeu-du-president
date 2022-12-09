import random
import string

import constant
from constant import VALUES, SUITS, NAMES
from itertools import combinations


class Card:
    """
    La classe Card qui permet d'initialiser les cartes avec leur valeur ('3', 'J', ...) et leur couleur ('♡', '♢', ...)
    et d'effectuer les comparaisons entre elles.
    """

    def __init__(self, value: string, suit: string):
        """
        Le constructeur de la classe Carte.
        Il n'existe pas de constructeur avec des valeurs par défaut. Les cartes ont forcément une couleur et une valeur.
        """
        self.__suit: string = suit
        self.__value: string = value

    @property
    def value(self):
        """
        Le getter de la valeur de la carte.
        """
        return self.__value

    @property
    def suit(self):
        """
        Le getter de la couleur de la carte.
        """
        return self.__suit

    def __eq__(self, other) -> bool:
        """
        La définition de l'opérateur d'égalité pour la classe Carte.
        Deux cartes sont égales si elles ont une valeur identique.
        """
        return self.__value == other.value

    def __lt__(self, other) -> bool:
        """
        La définition de l'opérateur strictement inférieur pour la classe Carte.
        La position d'une carte relativement à une autre est déterminée par sa position dans la liste constant.VALUES.
        Plus son index dans constant.VALUES est important, plus elle sera supérieure à d'autres cartes.
        """
        return VALUES.index(self.__value) < VALUES.index(other.value)

    def __ne__(self, other) -> bool:
        """
        La définition de l'opérateur d'inégalité pour la classe Carte.
        Deux cartes sont différentes si elles ont des valeurs différentes.
        """
        return self.__value != other.value

    def __gt__(self, other) -> bool:
        """
        La définition de l'opérateur strictement supérieur pour la classe Carte.
        La position d'une carte relativement à une autre est déterminée par sa position dans la liste constant.VALUES.
        Plus son index dans constant.VALUES est important, plus elle sera supérieure à d'autres cartes.
        """
        return VALUES.index(self.__value) > VALUES.index(other.value)

    def __str__(self):
        """
        La définition de __str__.
        str(Card('3', '♡')  = '3♡'
        """
        return self.__value + self.__suit


class Cards(list[Card]):
    """
    La classe Cards qui hérite de list[Card].
    C'est une liste de cartes où le mot-clé in (__contains__) est redéfini et qui ajoute des méthodes propres à ce type
    de liste.
    """

    def get_as_dict(self):
        """
        Retourne la liste de cartes self sous la forme d'un dictionnaire où :
        - la clé est la valeur de la carte ('3', '4', 'J', 'Q', ...),
        - la valeur est la liste des cartes de self ayant cette valeur.
        """
        cards_as_dict = {}
        for card in self:
            # Si la liste des cartes de la valeur est vide, on la crée.
            if card.value not in list(cards_as_dict.keys()):
                cards_as_dict[card.value] = [card]
            # Sinon, on lui ajoute les cartes déjà présentes.
            else:
                cards_as_dict[card.value] = [card] + cards_as_dict[card.value]
        return cards_as_dict

    def __contains__(self, card):
        """
        La définition de __contains__, c'est-à-dire du mot-clé in.
        La définition de l'égalité pour la classe Card entraîne qu'une carte d'une certaine valeur est contenue dans
        une liste de cartes dès lors qu'une carte de la même valeur y est, peu importe si la couleur correspond.
        Card('3', '♡') in [Card('3', '♢')] = True, ce qui est un problème.
        Cette définition de __contains__ tient compte de la valeur ET de la couleur des cartes.
        """
        cards_as_dict = self.get_as_dict()
        contain = False
        # si une carte de même valeur est présente dans self, on compare ensuite les couleurs
        if card.value in list(cards_as_dict.keys()):
            for card_same_value in cards_as_dict[card.value]:
                if card_same_value.suit == card.suit:
                    contain = True
        return contain

    def __str__(self):
        """
        La définition de __str__ de la classe Cards.
        Gère la manière dont est affichée un object Cards.
        """
        cards_str = ""
        for card in self:
            cards_str += f'{card} '
        return cards_str


class Deck:
    """
    La classe Deck. Un deck plein contient toutes les cartes qu'il peut mélanger.
    """

    def __init__(self):
        """
        Le constructeur de la classe Deck qui a pour attribut un Cards (une liste de carte évoluée).
        À l'initialisation, toutes les cartes possibles sont ajoutées une fois au deck.
        """
        self.__cards = Cards()
        for value in VALUES:
            for suit in SUITS:
                self.__cards.append(Card(value, suit))

    @property
    def cards(self):
        """
        Le getter des cartes du deck.
        """
        return self.__cards

    def __eq__(self, other):
        """
        La définition de l'opérateur d'égalité entre les decks.
        Deux decks sont égaux s'ils ont les mêmes cartes dans le même ordre.
        """
        return self.cards == other.cards

    def shuffle(self):
        """
        Mélange les cartes du deck.
        """
        random.shuffle(self.__cards)


class Trick:
    """
    La classe Trick contient toutes les informations contenant le pli et les opérations qu'on peut effectuer dessus.
    """

    def __init__(self):
        """
        Le constructeur de la classe Trick. Contient la liste des cartes, le nombre de cartes demandées pour le pli
        (initialisé à 0) et l'indice du dernier joueur à avoir posé une carte dans le pli (initialisé à -1).
        """
        self.__cards = Cards()
        self.__number_of_cards = 0
        self.__last_player_index = -1

    def add_cards(self, cards: Cards, player_index: int) -> None:
        """
        Ajoute les cartes données en paramètre aux cartes du pli.
        Met à jour le nombre de cartes demandées pour le pli s'il s'agit de la première carte jouée.
        Met à jour l'indice du dernier joueur à avoir posé une carte à partir du paramètre fourni en entrée.
        """
        if len(self.__cards) == 0:
            self.__number_of_cards = len(cards)
        self.__cards.extend(cards)
        self.__last_player_index = player_index

    @property
    def cards(self):
        """
        Le getter des cartes du pli.
        """
        return self.__cards

    @property
    def number_of_cards(self):
        """
        Le getter du nombre de cartes demandées pour le pli.
        """
        return self.__number_of_cards

    @number_of_cards.setter
    def number_of_cards(self, number):
        """
        Le setter du nombre de cartes demandées pour le pli.
        """
        self.__number_of_cards = number

    @property
    def last_player_index(self):
        """
        Le getter du nombre de cartes demandées pour le pli.
        """
        return self.__last_player_index

    def __str__(self):
        """
        La définition de __str__ de la classe Trick.
        Gère la manière dont est affichée un object Trick.
        """
        return f'[Trick\n\tCartes : {self.__cards}\n\tNombre de cartes demandées : {self.__number_of_cards}\n]'


class Player:
    """
    La classe Player qui contient toutes les informations concernant le joueur, ses cartes et les manipulations qu'il
    peut effectuer dessus.
    """

    def __init__(self, name: string = ""):
        """
        Le constructeur de la classe Player qui initialise son nom (en lui donnant une valeur au hasard parmi celles de
        constant.NAMES), sa main (ses cartes) et son rôle à la fin du tour (une valeur parmi celle de constant.ROLES),
        initialisé à None.
        """
        self._name: string = random.choice(NAMES) if name == "" else name
        self._hand = Cards()
        self._traded_cards = Cards()
        self._role = None

    @property
    def name(self):
        """
        Le getter du nom du joueur.
        """
        return self._name

    @property
    def hand(self):
        """
        Le getter de la main du joueur (ses cartes).
        """
        return self._hand

    @property
    def traded_cards(self):
        """
        Le getter des cartes que le joueur met à l'échange.
        """
        return self._traded_cards

    @property
    def role(self):
        """
        Le getter du rôle du joueur ("Trou", "Vice-Trou", etc.).
        """
        return self._role

    @role.setter
    def role(self, role: string):
        """
        Le setter du rôle du joueur ("Trou", "Vice-Trou", etc.).
        """
        self._role = role

    def add_to_hand(self, cards: Cards) -> None:
        """
        Ajoute la carte donnée en paramètre à la main du joueur.
        """
        for card in cards:
            self._hand.append(card)

    def remove_from_hand(self, cards: Cards) -> None:
        """
        Retire la carte donnée en paramètre de la main du joueur.
        """
        for card in cards:
            self._hand.remove(card)

    def clear_hand(self) -> None:
        """
        Vide la main du joueur.
        """
        self._hand = []

    def sort_hand(self) -> None:
        """
        Trie la main du joueur.
        """
        self.hand.sort()

    def has_card(self, card: Card) -> bool:
        """
        Retourne True si le joueur a en main la carte donnée en paramètre, False sinon.
        """
        return card in self._hand

    def play(self, cards: Cards) -> None:
        """
        Joue les cartes données en paramètres, i.e les retire de la main du joueur.
        """
        self.remove_from_hand(cards)

    def trade(self, cards: Cards) -> None:
        """
        Échange les cartes données en paramètres, i.e les retire de la main du joueur et les ajoute à ses cartes à
        échanger.
        """
        self._traded_cards = cards
        self.remove_from_hand(cards)

    def get_cards_allowed_to_play(self, trick: Trick) -> Cards:
        """
        Retourne la liste des cartes de la main du joueur que ce dernier peut jouer dans le respect des règles du jeu,
        au vu du pli en cours.
        """
        cards_allowed = Cards()
        # si le pli est vide, le joueur peut jouer toutes ses cartes
        if len(trick.cards) == 0:
            cards_allowed = self._hand
        # sinon
        else:
            trick.cards.sort()
            cards_as_dict = self._hand.get_as_dict()
            for value, cards in cards_as_dict.items():
                # le joueur ne peut jouer que les cartes qui ont une valeur supérieure à la plus grande du pli
                if cards[0] > trick.cards[-1] and \
                        len(cards) >= trick.number_of_cards:  # les cartes de la valeur doivent être plus nombreuses que
                                                              # le nombre de cartes que le pli attend
                    cards_allowed.extend(cards)
        return cards_allowed

    def get_cards_allowed_to_trade(self) -> Cards:
        """
        Retourne la liste des cartes de la main du joueur que ce dernier peut échanger en fonction de son rôle.
        """
        cards_allowed = Cards()
        self._hand.sort()
        hand_dict = self._hand.get_as_dict()
        if self._role == constant.FIRST or self._role == constant.SECOND:
            cards_allowed = self._hand
        elif self._role == constant.BEFORE_LAST or self._role == constant.LAST:
            max_value = max(self._hand).value
            cards_allowed = hand_dict[max_value]
        return cards_allowed

    def __str__(self):
        """
        La définition de __str__ de la classe Player.
        Gère la manière dont est affichée un object Player.
        """
        return f'[Joueur {self._name}\n\tCartes : {self._hand}\n\tRôle : {self._role}]'


class AIPlayer(Player):
    """
    La classe AIPlayer qui hérite de la classe Player et définit des comportements automatiques de jeu.
    """

    def __init__(self, name: string = ''):
        """
        Le constructeur de la classe AIPlayer, identique à la classe parent.
        """
        super().__init__(name)

    def random_cards_to_play(self, trick: Trick) -> Cards:
        """
        Joue des cartes ou passe son tour au hasard en respectant les règles au vu du pli donné en entrée.
        """
        # récupère les cartes autorisées sous forme d'un dictionnaire
        cards_allowed = self.get_cards_allowed_to_play(trick)
        cards_allowed_dict = cards_allowed.get_as_dict()
        # choisit au hasard une valeur parmi celles qui sont autorisées
        values = list(cards_allowed_dict.keys())
        random_value = random.choice(values)
        # la liste des cartes de la main de l'IA qui ont la valeur retenue
        cards_allowed_value = cards_allowed_dict[random_value]
        # si ce n'est pas le début du tour (la liste des cartes du pli n'est pas vide)
        if len(trick.cards) != 0:
            # récupère une liste de toutes les combinaisons des cartes de la valeur choisie de longueur le nombre de
            # cartes demandées pour le pli
            cards_combination_allowed = list(combinations(cards_allowed_value, trick.number_of_cards))
            # ajoute une liste vide, si elle est retenue, l'IA passe son tour
            cards_combination_allowed.append([])
        # si c'est le début du tour
        else:
            # récupère la liste de toutes les combinaisons possibles de longueur au moins 1 des cartes de la valeur
            # choisie.
            nb_cards_with_value = len(cards_allowed_value)
            cards_combination_allowed = [list(comb) for nb_cards in range(1, nb_cards_with_value + 1)
                                         for comb in combinations(cards_allowed_value, nb_cards)]
        # retourne un objet Cards, choisi aléatoirement parmi les combinaisons retenues.
        return Cards(random.choice(cards_combination_allowed))

    def random_cards_to_trade(self):
        """
        Retourne au hasard des cartes à échanger parmi celles qui ont la plus petite valeur.
        """
        cards_allowed = self.get_cards_allowed_to_trade()
        cards_allowed_dict = cards_allowed.get_as_dict()
        nb_cards_to_trade = 0
        if self._role == constant.FIRST or self._role == constant.LAST:
            nb_cards_to_trade = 2
        elif self._role == constant.SECOND or self._role == constant.BEFORE_LAST:
            nb_cards_to_trade = 1
        min_value = min(cards_allowed).value
        cards_to_trade = cards_allowed_dict[min_value]
        cards_combinations_allowed = list(combinations(cards_to_trade, nb_cards_to_trade))
        return Cards(random.choice(cards_combinations_allowed))


class PresidentGame:
    """
    La classe PresidentGame qui contient toute l'information sur la partie et gère les opérations qui peuvent être
    effectuées dessus.
    """

    def __init__(self, players: list[Player] = None, number_of_sets: int = 1):
        """
        Le constructeur de la classe PresidentGame. Crée par défaut une liste de 3 joueurs, initialise les variables et
        commence la première manche.
        """
        self.__players = [Player(), Player(), Player()] if players is None else players
        self.__current_trick: Trick = Trick()
        self.__current_player_index: int = 0
        self.__turns_without_plays: int = 0
        self.__number_of_sets: int = number_of_sets
        self.__current_set: int = 0
        self.__players_without_card: list[Player] = []
        self.__is_trade = False
        self.__nb_players_traded = 0
        self.start_set()

    @property
    def players(self):
        """
        Le getter de la liste des joueurs de la partie.
        """
        return self.__players

    @property
    def current_trick(self):
        """
        Le getter du pli en cours de la partie.
        """
        return self.__current_trick

    @property
    def current_player_index(self):
        """
        Le getter de l'indice du joueur de qui c'est le tour.
        """
        return self.__current_player_index

    @current_player_index.setter
    def current_player_index(self, index: int):
        """
        Le setter de l'indice du joueur de qui c'est le tour.
        """
        self.__current_player_index = index

    @property
    def turns_without_plays(self):
        """
        Le getter du nombre de tours consécutifs sans qu'aucune carte n'ait été jouée (dans un même pli).
        """
        return self.__turns_without_plays

    @property
    def current_set(self):
        """
        Le getter de la manche en cours.
        """
        return self.__current_set

    @property
    def is_trade(self):
        """
        Le getter du booléen qui indique si on est dans la phase d'échange des cartes ou non
        """
        return self.__is_trade

    def get_current_player(self):
        """
        Retourne le joueur dont l'indice est celui du joueur dont c'est le tour (un attribut de classe)
        """
        return self.__players[self.__current_player_index]

    def start_set(self) -> None:
        """
        Commence la manche, c'est-à-dire distribue et détermine qui est le joueur qui commence à jouer.
        """
        # distribue les cartes
        self.distribute()
        # s'il s'agit de la première manche de la partie
        if self.__current_set == 0:
            # puis détermine qui commence, i.e le joueur qui a la dame de cœur.
            for index, player in enumerate(self.__players):
                if player.has_card(Card("Q", "♡")):
                    self.__current_player_index = index

    def distribute(self):
        """
        Mélange le deck, distribue les cartes aux joueurs et ordonne chacune des cartes.
        """
        deck = Deck()
        deck.shuffle()
        cards = deck.cards
        number_of_players = len(self.players)
        for index, card in enumerate(cards):
            # commence la distribution par le joueur qui ouvre la manche (il fait partie de ceux qui ont le plus de
            # cartes)
            player = self.players[(index + self.__current_player_index) % number_of_players]
            player.add_to_hand(Cards([card]))
        # trie les cartes de chaque joueur
        for player in self.__players:
            player.hand.sort()

    def add_cards_to_trade(self, cards: Cards):
        """
        Ajoute les cartes en paramètre aux cartes du joueur courant à échanger
        """
        self.get_current_player().trade(cards)
        self.__nb_players_traded += 1

    def is_trade_over(self):
        """
        Retourne True si les échanges de cartes sont terminés, i.e si tous les joueurs sauf les neutres ont mis des
        cartes à l'échange.
        """
        roles = constant.ROLES[len(self.__players)]
        return self.__nb_players_traded == [role for role in roles if role != constant.NEUTRAL]

    def trade_cards(self):
        """
        Échange les cartes entre les joueurs, entre trou et président, et entre vice-trou et vice-président
        """
        president = self.__players_without_card[0]
        trou = self.__players_without_card[-1]
        president.add_to_hand(trou.traded_cards)
        trou.add_to_hand(president.traded_cards)

        if len(self.__players) > 3:
            vice_president = self.__players_without_card[1]
            vice_trou = self.__players_without_card[-2]
            vice_president.add_to_hand(vice_trou.traded_cards)
            vice_trou.add_to_hand(vice_president.traded_cards)

        self.__is_trade = False

    def next_player(self):
        """
        Passe la main au joueur suivant. Augmente l'indice du joueur dont c'est le tour de 1.
        Revient à 0 si l'indice atteint le nombre de joueurs de la partie.
        """
        self.__current_player_index = (self.__current_player_index + 1) % len(self.__players)

    def skip_turn(self):
        """
        Passe le tour du joueur. Augmente le nombre de tours sans cartes jouées de 1.
        """
        self.__turns_without_plays += 1

    def play(self, cards: Cards) -> None:
        """
        Le joueur courant joue les cartes données en paramètre.
        """
        # remet à 0 le nombre de tours sans cartes jouées consécutif.
        self.__turns_without_plays = 0
        current_player = self.get_current_player()
        # retire les cartes du joueur courant
        current_player.play(cards)
        # ajoute les cartes à celles du pli en cours
        self.__current_trick.add_cards(cards, self.__current_player_index)
        # si le joueur n'a plus de cartes, détermine le rôle du joueur
        if len(current_player.hand) == 0:
            self.__players_without_card.append(current_player)

    def is_turn_ended(self) -> bool:
        """
        Retourne True si le tour est terminé, false sinon.
        Un tour est terminé si le pli n'est pas vide et si :
        - soit tous les joueurs ont passé consécutivement,
        - soit si la plus haute carte jouée est un 2.
        """
        self.__current_trick.cards.sort()
        return not len(self.__current_trick.cards) == 0 \
               and (self.__turns_without_plays >= len(self.__players)
                    or self.__current_trick.cards[-1].value == 2)

    def end_turn(self) -> None:
        """
        Termine le tour, i.e réinitialise les variables.
        Le joueur qui commence le tour suivant est celui qui a posé la dernière carte du précédent.
        """
        self.__current_player_index = self.__current_trick.last_player_index
        self.__current_trick = Trick()
        self.__turns_without_plays = 0

    def is_set_ended(self) -> bool:
        """
        Retourne True si la manche est finie, i.e s'il reste des cartes à un seul joueur, False sinon.
        """
        return len(self.__players_without_card) == len(self.__players) - 1

    def end_set(self) -> None:
        """
        Termine la manche, i.e désigne le trou, le désigne comme premier joueur de la manche suivante et vide sa main.
        """
        for index, player in enumerate(self.__players):
            if len(player.hand) != 0:
                self.__current_player_index = index
                player.clear_hand()
                self.__players_without_card.append(player)
        self.assign_role()
        self.__current_set += 1
        self.__is_trade = True

    def assign_role(self) -> None:
        """
        Assigne un rôle au joueur donné en paramètre.
        Dépend du nombre de joueurs de la partie et du nombre de joueurs qui n'ont déjà plus de cartes.
        """
        nb_players = len(self.__players)
        for index, player in enumerate(self.__players_without_card):
            player.role = constant.ROLES[nb_players][index]

    def is_game_ended(self) -> bool:
        """
        Retourne True si la partie est finie, c'est-à-dire si le nombre de manches fixées à l'avance est atteint,
        False sinon.
        """
        return self.__current_set >= self.__number_of_sets

    def end_game(self):
        pass

    def __str__(self):
        """
        La définition de __str__ de la classe Player.
        Gère la manière dont est affichée un object Player.
        """
        players_str = ""
        for player in self.__players:
            players_str += f'{player}\n'
        return f"Joueurs : \n{players_str}" \
               f"\nPli en cours:" \
               f"\n{self.__current_trick}" \
               f"\nTour de {self.__players[self.__current_player_index].name}" \
               f"\nManche {self.__current_set + 1}" \
               f"\nNombre de manches total : {self.__number_of_sets}" \
               f"\nNombre de tours sans cartes jouées : {self.__turns_without_plays}"
