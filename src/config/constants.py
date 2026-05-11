"""Configuration constants for the Wordle game."""

from pathlib import Path

# Game constants
WORD_LENGTH = 5
MAX_GUESSES = 6
DAYS_SINCE_EPOCH = 18628  # Days since Jan 1, 1970 to Jan 1, 2021

# File paths
DATA_DIR = Path('/workspace/term-wordle-8049/src/config/data')
WORDS_FILE = DATA_DIR / 'words.txt'
VALID_WORDS_FILE = DATA_DIR / 'valid_words.txt'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
