SUITS = ['♡', '♤', '♢', '♧']
VALUES = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
NAMES = ['Robert', 'Françoise', 'Michel', 'Isabelle', 'Damien', 'Fatima', 'Alphonse', 'Brigitte', 'Kevin', 'Gilles',
         'Mehdi']

FIRST = "Président"
SECOND = "Vice-président"
NEUTRAL = "Neutre"
BEFORE_LAST = "Vice-trou"
LAST = "Trou"

ROLES = {
    3: [FIRST, NEUTRAL, LAST],
    4: [FIRST, SECOND, BEFORE_LAST, LAST],
    5: [FIRST, SECOND, NEUTRAL, BEFORE_LAST, LAST],
    6: [FIRST, SECOND, NEUTRAL, NEUTRAL, BEFORE_LAST, LAST]
}

