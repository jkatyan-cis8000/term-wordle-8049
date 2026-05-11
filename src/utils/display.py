"""Utility functions for the Wordle game."""

from typing import Iterable

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
GREY = '\033[90m'
RESET = '\033[0m'


def color_letter(letter: str, state: str) -> str:
    """Color a letter based on its state."""
    if state == 'green':
        return f"{GREEN}{letter}{RESET}"
    elif state == 'yellow':
        return f"{YELLOW}{letter}{RESET}"
    elif state == 'grey':
        return f"{GREY}{letter}{RESET}"
    return letter


def color_guess(guess: str, result: Iterable[str]) -> str:
    """Color an entire guess based on the result states."""
    return ''.join(color_letter(letter, state) for letter, state in zip(guess, result))


def format_board(guesses: list[tuple[str, list[str]]]) -> str:
    """Format the game board for display."""
    lines = []
    for guess, result in guesses:
        lines.append(color_guess(guess, result))
    return '\n'.join(lines)


def get_console_width() -> int:
    """Get the console width for formatting output."""
    return 80


def center_text(text: str, width: int | None = None) -> str:
    """Center text within a given width."""
    if width is None:
        width = get_console_width()
    return text.center(width)
