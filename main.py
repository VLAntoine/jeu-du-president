import model


# deck1 = model.Deck()
# deck2 = model.Deck()

player1 = model.Player()
player2 = model.Player()
player3 = model.Player()
player4 = model.Player()

game = model.PresidentGame( players = [player1 ,player2 ,player3 ,player4] )


print("player 1 - ", player1.name, " have this hand : ")
for card in player1.hand:
    print(card.value, card.suit)

print("player 2 - ", player2.name, " have this hand : ")
for card in player2.hand:
    print(card.value, card.suit)

print("player 3 - ", player3.name, " have this hand : ")
for card in player3.hand:
    print(card.value, card.suit)

print("player 4 - ", player4.name, " have this hand : ")
for card in player4.hand:
    print(card.value, card.suit)

# print("DECK1 : ")
# print(deck1)
# print("\n")
# print("DECK2 : ")
# print(deck2)
# print("\n")
