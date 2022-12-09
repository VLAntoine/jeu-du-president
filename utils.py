from constant import VALUES, SUITS, FIRST, SECOND, BEFORE_LAST, LAST, NEUTRAL
from exception import WrongRequestException, NotInRulesException
from model import PresidentGame, Cards


def check_request(request: dict):
    """
    Vérifie la validité de la requête transmise par l'utilisateur du point de vue de la forme.
    Lève une exception si elle n'est pas valide.
    """

    # la requête doit contenir une clé skip qui est un booléen
    if 'skip' not in list(request.keys()) and isinstance(request['skip'], bool):
        raise WrongRequestException("La requête doit contenir une entrée 'skip', vraie ou fausse.")

    # si la valeur associée à skip est fausse
    if not request['skip']:
        # la requête doit contenir une liste de cartes non vide
        if 'cards' not in list(request.keys()) and \
                isinstance(request['cards'], list) and \
                len(request['cards']) == 0:
            raise WrongRequestException("Vous avez passé, vous devez fournir une liste de cartes")

        # les cartes doivent être de la forme '{value}{suit}'
        if not all((card[0] in VALUES and card[1] in SUITS) for card in request['cards']):
            raise WrongRequestException("Les cartes doivent être de la forme '{valeur}{couleur}'.")


def check_skip(game: PresidentGame):
    """
    Vérifie si l'utilisateur a le droit de passer, du point de vue des règles.
    Lève une exception s'il n'a pas le droit.
    """
    # le joueur ne peut pas passer s'il est le premier du pli à jouer
    if len(game.current_trick.cards) == 0:
        raise NotInRulesException("Vous êtes le premier à jouer, vous ne pouvez pas passer.")


def check_cards(game: PresidentGame, cards: Cards):
    """
    Vérifie si l'utilisateur possède les cartes données en paramètres, du point de vue des règles.
    Lève une exception s'il n'a pas le droit.
    """
    # le joueur ne possède pas les cartes qu'il joue ou met à l'échange
    if not all(card in game.get_current_player().hand for card in cards):
        "Vous n'avez pas en main toutes les cartes que vous jouez"


def check_play(game: PresidentGame, cards: Cards):
    """
    Vérifie si l'utilisateur a le droit de jouer les cartes données en paramètres, du point de vue des règles.
    Lève une exception s'il n'a pas le droit.
    """
    # les cartes n'ont pas toutes la même valeur
    if not all(card == cards[0] for card in cards):
        raise NotInRulesException("Vous devez jouer des cartes qui ont toutes la même valeur.")

    # la valeur de la carte jouée est inférieure à la dernière carte jouée
    if len(game.current_trick.cards) != 0 and cards[0].value < max(game.current_trick.cards).value:
        raise NotInRulesException("Vous devez une carte plus forte ou égale à la plus forte du pli.")

    # le nombre de cartes jouées ne correspond pas au nombre de cartes attendues pour le pli courant
    if len(game.current_trick.cards) != 0 and len(cards) != game.current_trick.number_of_cards:
        raise NotInRulesException("Le nombre de cartes attendues pour ce pli est différent du nombre de cartes que "
                                  "vous jouez.")


def check_trade(game: PresidentGame, cards: Cards):
    """
    Vérifie si l'utilisateur a le droit d'échanger les cartes données en paramètres, du point de vue des règles.
    Lève une exception s'il n'a pas le droit.
    """
    current_player = game.get_current_player()
    cards.sort()

    # le joueur est neutre et n'a pas à échanger de cartes
    if current_player.role == NEUTRAL:
        raise NotInRulesException("Vous êtes neutre, vous n'avez pas à échanger de cartes.")

    # le joueur ne donne pas le bon nombre de cartes à échanger
    if ((current_player.role == FIRST or current_player.role == LAST) and len(cards) != 2) or \
            ((current_player.role == SECOND or current_player.role == BEFORE_LAST) and len(cards) != 1):
        raise NotInRulesException("Vous n'échangez pas le bon nombre de cartes.")

    # le joueur est trou ou vice-trou et ne donne pas ses plus grandes cartes
    if (current_player.role == BEFORE_LAST and cards[0].value != current_player.hand[-1].value) or \
            (current_player.role == LAST and
             ((cards[-1].value != current_player.hand[-1].value) or (
                     cards[-2].value != current_player.hand[-2].value))):
        raise NotInRulesException("Vous devez échanger vos meilleures cartes.")
