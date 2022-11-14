from constant import VALUES, SUITS
from exception import WrongRequestException, NotInRulesException
from model import PresidentGame


def check_request(request: dict, game: PresidentGame):
    if not request["player_index"]:
        raise WrongRequestException("La requête doit contenir un joueur")

    if not request["skip"] and \
            (not request["cards"]["value"] or not request["cards"]["suits"]) and \
            (request["cards"]["value"] not in VALUES or
             all(suit in SUITS for suit in request["cards"]["suits"])):
        raise WrongRequestException("La requête doit soit contenir skip, soit une liste de cartes valables")
        # c'est bien au tour du joueur qui joue de jouer
    if request["player"] != game.current_player_index:
        raise NotInRulesException("Ce n'est pas à votre tour de jouer")
    # la valeur de la carte jouée est supérieure à la dernière carte jouée
    if request["cards"]["value"] > max(game.current_trick.cards).value:
        raise NotInRulesException("La valeur de la carte envoyée est inférieure à la carte la plus forte du pli")
    # le nombre de cartes jouées correspond au nombre de cartes attendues pour le pli courant
    if len(request["cards"]["suits"]) != game.current_trick.number_of_cards:
        raise NotInRulesException("Le nombre de cartes attendues pour ce pli est différent du nombre de cartes que "
                                  "vous jouez")



