"""Type definitions for the Wordle game."""

from enum import Enum
from typing import NewType, Tuple


# Valid English words (loaded at runtime)
Word = NewType('Word', str)

# A 5-letter guess word
Guess = NewType('Guess', str)


class LetterState(Enum):
    """State of a letter in a guess."""
    GREEN = 'green'      # Correct letter in correct position
    YELLOW = 'yellow'    # Correct letter in wrong position
    GREY = 'grey'        # Letter not in word


GuessResult = Tuple[LetterState, ...]
"""A tuple of 5 LetterState values representing the result of a guess."""
