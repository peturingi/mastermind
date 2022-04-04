import random
from functools import cached_property
from typing import List, Optional

from game import Player, Pattern, Hint, Symbol, Game


class DonaldKnuth(Player):
    def __init__(self):
        super().__init__("Donald Knuth")
        self._hint: Optional[Hint] = None
        self._possible_codes: Optional[List[Pattern]] = []
        self._previous_guess: Optional[Pattern] = None
        self._reset_guess_algorithm()
        
    def create_codeword(self):
        self._codeword = Pattern(*[Symbol(random.choice(list(Symbol))) for _ in range(4)])
        self._reset_guess_algorithm() # Step 1. Create the Set of 1296 possible codes.
        
    def _reset_guess_algorithm(self):
        self._hint = None
        self._possible_codes = self._all_possible_codes
        
    @cached_property
    def _all_possible_codes(self) -> List[Pattern]:
        all_possible_codes = []
        symbols = range(1, 7)
        # todo replace with cartesian product of [1;6]
        for a in symbols:
            for b in symbols:
                for c in symbols:
                    for d in symbols:
                        all_possible_codes.append(Pattern(*[Symbol(i) for i in (a, b, c, d)]))
        return all_possible_codes

    def take_hint(self, hint: Hint) -> None:
        super().take_hint(hint)
        self._hint = hint
        
        # Step 4. If the response is four colored pegs, the game is won, the algorithm terminates.
        if self._hint == Game.WIN_CONDITION:
            self._possible_codes = None
            self._previous_guess = None
            return
        
        # Step 5. Otherwise, remove from S any code that
        # would not give the same response if it (the guess) were the code.
        codes_to_remove = []
        for possible_code in self._possible_codes:
            self._codeword = possible_code
            if hint != self.give_hint(self._previous_guess):
                codes_to_remove.append(possible_code)
        self._codeword = None
        for r in codes_to_remove:
            self._possible_codes.remove(r)
        
    def guess(self) -> Pattern:
        # Step 2. "Start with initial guess 1122".
        # Step 3. "Play the guess to get a response of coloured and white pegs."
        if self._previous_guess is None:
            guess = Pattern(*[Symbol(i) for i in (1, 1, 2, 2)])
            self._previous_guess = guess
            self._possible_codes.remove(guess)
            return guess
        else:
            # TODO Implement step 6; minimax self._possible_codes
            self._previous_guess = guess = self._possible_codes.pop()
            return guess