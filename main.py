import view
import model

number_of_players = input("Combien de joueurs pour cette partie ? (minimum 4) ")
nb_players = int(number_of_players) - 1
number_of_sets = input("En combien de sets se jouera la partie ? ")
players :list = []

print("nb de joueur : ", nb_players)

while nb_players >= 1:
    player = model.Player()
    players.append(player)
    nb_players = nb_players - 1
    print(nb_players)

print("players : ", len(players))

console_view = view.CommandLineView(players, number_of_sets)
