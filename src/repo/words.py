"""Word repository for loading and selecting daily words."""

import random
from datetime import date
from pathlib import Path

from ..types.wordle import Word


def load_words(filepath: Path) -> list[Word]:
    """Load words from a file, one word per line."""
    words = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().upper()
            if word and len(word) == 5:
                words.append(Word(word))
    return words


def get_daily_word(words: list[Word], target_date: date | None = None) -> Word:
    """Select the daily word based on the current date."""
    if target_date is None:
        target_date = date.today()
    
    # Calculate days since a fixed epoch (Jan 1, 2021)
    epoch = date(2021, 1, 1)
    days_since_epoch = (target_date - epoch).days
    
    # Use deterministic selection based on date
    random.seed(days_since_epoch)
    index = random.randint(0, len(words) - 1)
    return words[index]


def select_word(words: list[Word]) -> Word:
    """Select a random word from the list."""
    random.seed()  # Reset to random seed
    index = random.randint(0, len(words) - 1)
    return words[index]
