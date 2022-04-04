from enum import IntEnum, unique
from typing import Tuple, List
from collections import Counter

@unique
class Symbol(IntEnum):
    BLUE = 1
    GREEN = 2
    ORANGE = 3
    PURPLE = 4
    RED = 5
    YELLOW = 6

@unique
class _Hit(IntEnum):
    EMPTY = 0
    """Symbol not in codeword."""
    WHITE = 1
    """Symbol in codeword; wrong position."""
    BLACK = 2
    """Symbol in codeword; correct position."""

class Hint:
    def __init__(self, hits: Tuple[_Hit, _Hit, _Hit, _Hit]):
        self._hits = hits

    def __eq__(self, other):
        return isinstance(other, Hint) and set(self._hits) == set(other._hits)
    
    def __str__(self):
        return " ".join([hit.name for hit in self._hits if hit is not _Hit.EMPTY])
    
    def __hash__(self):
        return hash(str(self))


class Pattern:
    def __init__(self, first: Symbol, second: Symbol, third: Symbol, fourth: Symbol):
        self._symbols = (first, second, third, fourth)
        
    @property
    def symbols(self) -> Tuple[Symbol, Symbol, Symbol, Symbol]:
        return self._symbols
    
    def __hash__(self):
        return hash(self._symbols)
    
    def __eq__(self, other):
        return isinstance(other, Pattern) and self._symbols == other._symbols
    
    def __str__(self):
        return str(self.symbols)
    
    def __repr__(self):
        return str(self)


class Player:
    def __init__(self, name: str):
        self._score = 0
        self.name = name
        self._codeword = None
    
    @property
    def score(self) -> int:
        return self._score
        
    def add_score(self, score: int):
        assert 1 <= score <= Game.MAX_ATTEMPTS_TO_BREAK_CODE
        self._score += score
        
    def create_codeword(self):
        codeword = input(f"{self.name} codeword: ")
        # todo error handle input
        self._codeword = Pattern(*[Symbol(int(char)) for char in codeword])

    def take_hint(self, hint: Hint) -> None:
        print(hint)
        
    def give_hint(self, guess: Pattern) -> Hint:
        codeword_counter = Counter(self._codeword.symbols)
        blacks = sum([int(self._codeword.symbols[i] == guess.symbols[i]) for i in range(0, len(guess.symbols))])
        whites = codeword_counter.total() - (codeword_counter - Counter(guess.symbols)).total() - blacks
        return Hint(tuple([_Hit.BLACK] * blacks + [_Hit.WHITE] * whites + [_Hit.EMPTY] * (4 - blacks - whites)))
    
    def guess(self) -> Pattern:
        guess=input(f"{self.name} guess: ")
        # todo error handle input
        symbols = [Symbol(int(c)) for c in guess]
        return Pattern(*symbols)
    
    def __str__(self):
        return self.name


class Game:
    MAX_ATTEMPTS_TO_BREAK_CODE = 9
    WIN_CONDITION = Hint((_Hit.BLACK, _Hit.BLACK, _Hit.BLACK, _Hit.BLACK))
    
    def __init__(self, codemaker: Player, codebreaker: Player):
        self._codemaker = codemaker
        self._codebreaker = codebreaker
    
    @property
    def _players(self) -> List[Player]:
        """Get players ordered by name."""
        return sorted([self._codemaker, self._codebreaker], key=lambda player: player.name)
    
    @property
    def score(self) -> str:
        return " -- ".join([f"{player.name} ({player.score})" for player in self._players])
        
    def switch_roles(self) -> None:
        self._codemaker, self._codebreaker = self._codebreaker, self._codemaker
    
    def _play(self) -> None:
        self._codemaker.create_codeword()
        codebreaking_attempts = 0
        while codebreaking_attempts < self.MAX_ATTEMPTS_TO_BREAK_CODE:
            codebreaking_attempts += 1
            guess = self._codebreaker.guess()
            hint = self._codemaker.give_hint(guess)
            self._codebreaker.take_hint(hint)
            if hint == self.WIN_CONDITION:
                print(f"{self._codebreaker.name} guessed correct in {codebreaking_attempts} attempts.")
                break
        else:
            print(f"{self._codemaker.name} won")
        
        self._codemaker.add_score(codebreaking_attempts)
        
    def run(self):
        while True:
            self._play()
            print(f"Score: {self.score}.")
            self.switch_roles()
