"""CLI interface for the Wordle game."""

import sys
from typing import Iterable

from ..types.wordle import Word
from ..service.game import WordleGame
from ..config.constants import WORD_LENGTH, MAX_GUESSES


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


def clear_screen() -> None:
    """Clear the terminal screen."""
    print('\033[2J\033[H', end='')


def print_header(title: str) -> None:
    """Print a centered header."""
    print(center_text(title))
    print()


def print_board(game: WordleGame) -> None:
    """Print the current game board."""
    state = game.get_state()
    guesses = state.get_guesses()
    
    if guesses:
        print(format_board(guesses))
    else:
        # Print empty rows for initial state
        for _ in range(MAX_GUESSES):
            print(' _ ' * WORD_LENGTH)
    print()


def print_feedback(message: str) -> None:
    """Print a feedback message."""
    print(message)
    print()


def get_user_guess() -> Word:
    """Get a guess from the user."""
    while True:
        guess = input("Enter your 5-letter guess: ").strip().upper()
        if len(guess) != WORD_LENGTH:
            print_feedback(f"Please enter a word with exactly {WORD_LENGTH} letters.")
            continue
        if not guess.isalpha():
            print_feedback("Please enter only letters.")
            continue
        return Word(guess)


def print_win(game: WordleGame) -> None:
    """Print win message."""
    state = game.get_state()
    num_guesses = len(state.guesses)
    print()
    print(center_text(f"YOU WON in {num_guesses} guesses!"))
    print()


def print_loss(game: WordleGame) -> None:
    """Print loss message."""
    target = game.reveal_word()
    print()
    print(center_text(f"GAME OVER! The word was: {target}"))
    print()


def play_turn(game: WordleGame) -> bool:
    """Play a single turn. Returns True if game should continue."""
    print_board(game)
    
    guess = get_user_guess()
    result = game.make_guess(guess)
    
    # Check if game ended
    state = game.get_state()
    if state.game_over:
        print_board(game)
        if state.game_won:
            print_win(game)
        else:
            print_loss(game)
        return False
    
    # Check if player ran out of guesses
    if state.attempts_remaining == 0:
        print_board(game)
        print_loss(game)
        return False
    
    print()
    return True


def play_game() -> None:
    """Main game loop."""
    game = WordleGame()
    game.start_game()
    
    print_header("WELCOME TO WORDLE!")
    print(center_text(f"You have {MAX_GUESSES} attempts to guess the daily word."))
    print(center_text("Green = correct letter, correct position"))
    print(center_text("Yellow = correct letter, wrong position"))
    print(center_text("Grey = letter not in word"))
    print()
    
    while play_turn(game):
        pass
    
    print(center_text("Thanks for playing!"))
    print()


def main() -> int:
    """Entry point for the CLI."""
    try:
        play_game()
        return 0
    except KeyboardInterrupt:
        print()
        print(center_text("Game interrupted. Goodbye!"))
        return 130


if __name__ == '__main__':
    sys.exit(main())
