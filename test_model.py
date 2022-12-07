import unittest

import model


class TestCards(unittest.TestCase):
    def test_card_constructor(self):
        self.assertTrue(isinstance(model.Card('A', '♡'), model.Card))

    def test_cards_equal_value(self):
        ace_of_hearts = model.Card('A', '♡')
        ace_of_spades = model.Card('A', '♤')
        self.assertEqual(ace_of_hearts, ace_of_spades, 'Two cards having '
                                                       'same value should be considered equal')

    def test_cards_comparison(self):
        ace_of_hearts = model.Card('A', '♡')
        two_of_hearts = model.Card('2', '♡')
        five_of_hearts = model.Card('5', '♡')
        five_of_spades = model.Card('5', '♤')

        self.assertTrue(ace_of_hearts > five_of_hearts)
        self.assertTrue(two_of_hearts > ace_of_hearts > five_of_hearts,
                        'The two card is the highest card')
        self.assertTrue(five_of_hearts < two_of_hearts,
                        'The two card is the highest card')
        self.assertEqual(five_of_hearts, five_of_spades,
                         "Two cards with same values are equal")
        self.assertNotEqual(ace_of_hearts, two_of_hearts,
                            "Two cards with different values are different")


class TestDeck(unittest.TestCase):
    def test_deck_has_52_cards(self):
        deck = model.Deck()
        self.assertEqual(len(deck.cards), 52, 'The president is a card game '
                                              'requiring 52 cards')

    def test_deck_shuffling(self):
        deck_1 = model.Deck()
        deck_2 = model.Deck()
        self.assertEqual(deck_1, deck_2, 'A new deck should not be automatically shuffled')
        deck_2.shuffle()
        self.assertNotEqual(deck_1, deck_2, 'Shuffling a deck '
                                            'randomizes the '
                                            'cards order')


class TestPlayer(unittest.TestCase):
    def test_player_constructor(self):
        player_trump = model.Player('Trump')
        self.assertTrue(player_trump.name == 'Trump')

    def test_incognito_player_should_have_random_name(self):
        player_incognito = model.Player()
        self.assertFalse(player_incognito.name == '')

    def test_add_card_to_hand(self):
        player = model.Player()
        ace_of_hearts = model.Card('A', '♡')
        player.add_to_hand(ace_of_hearts)
        self.assertEqual(player.hand, [ace_of_hearts],
                         "A card added to a player is added to it hand")
        self.assertTrue(player.has_card(ace_of_hearts),
                        "The player whose hand contains a card has this card")

    def test_remove_card_from_hand(self):
        player = model.Player()
        ace_of_hearts = model.Card('A', '♡')
        player.add_to_hand(ace_of_hearts)
        player.remove_from_hand(ace_of_hearts)
        self.assertEqual(player.hand, [],
                         "A card removed from a player is removed from it hand")


class TestTrick(unittest.TestCase):

    def test_new_trick_has_empty_hand(self):
        empty_trick = model.Trick()
        self.assertEqual(len(empty_trick.cards), 0,
                         "A new trick is empty")

    def test_add_one_card_to_trick(self):
        ace_of_hearts = model.Card('A', '♡')
        ace_of_spades = model.Card('A', '♤')
        two_of_hearts = model.Card('2', '♡')
        trick = model.Trick()
        trick.add_cards([ace_of_hearts])
        self.assertEqual(trick.number_of_cards, 1,
                         "The first card added to the trick define the number of cards of the trick")
        self.assertEqual(trick.cards, [ace_of_spades],
                         "Trick cards are equal to another with the same amount of cards of every value")
        self.assertNotEqual(trick.cards, [two_of_hearts],
                            "Trick cards are not equal to another with cards of different values")
        self.assertNotEqual(trick.cards, [ace_of_spades, ace_of_hearts],
                            "Trick cards are not equal to another with a different amount of cards")

        trick.add_cards([two_of_hearts])
        self.assertEqual(trick.number_of_cards, 1,
                         "A second card added to the trick doesn't change the number of cards of the trick")
        self.assertEqual(trick.cards, [ace_of_spades, two_of_hearts],
                         "Trick cards are equal to another with the same amount of cards of every value")

    def test_add_two_cards_to_trick(self):
        ace_of_hearts = model.Card('A', '♡')
        ace_of_spades = model.Card('A', '♤')
        trick = model.Trick()
        trick.add_cards([ace_of_hearts, ace_of_spades])
        self.assertEqual(trick.number_of_cards, 2,
                         "The first cards added to the trick define the number of cards of the trick")


class TestPresidentGame(unittest.TestCase):
    def test_default_game_has_three_players(self):
        game = model.PresidentGame()
        self.assertTrue(len(game.players) == 3)

    def test_game_launch_distributes_cards(self):
        """ Game generation should distribute cards evenly. """
        game = model.PresidentGame()
        player_1 = game.players[0]
        player_2 = game.players[1]
        print(player_1.hand)
        self.assertTrue(len(player_1.hand) > 0)
        self.assertTrue(len(player_1.hand) >= len(player_2.hand))

    def test_starting_game_has_empty_trick(self):
        game = model.PresidentGame()
        self.assertTrue(len(game.current_trick.cards) == 0)
