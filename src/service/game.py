"""Game service for Wordle logic and state management."""

from typing import Optional

from ..types.wordle import Word, Guess, LetterState, GuessResult
from ..config.constants import WORD_LENGTH, MAX_GUESSES
from ..repo.words import load_words, get_daily_word
from ..providers.random import choice, randint


class GameState:
    """Represents the current state of a Wordle game."""

    def __init__(self, target_word: Word) -> None:
        """Initialize game state with the target word."""
        self.target_word = target_word
        self.guesses: list[tuple[Guess, GuessResult]] = []
        self.attempts_remaining = MAX_GUESSES
        self.game_won = False
        self.game_over = False

    def is_valid_word(self, word: Word) -> bool:
        """Check if a word is valid (5 letters, all alphabetic)."""
        if len(word) != WORD_LENGTH:
            return False
        return word.isalpha()

    def evaluate_guess(self, guess: Guess) -> GuessResult:
        """Evaluate a guess and return the result."""
        result: list[LetterState] = []
        target_chars = list(self.target_word)
        guess_chars = list(guess)
        
        # First pass: find greens (correct position)
        for i in range(WORD_LENGTH):
            if guess_chars[i] == target_chars[i]:
                result.append(LetterState.GREEN)
                target_chars[i] = None  # Mark as used
                guess_chars[i] = None  # Mark as matched
            else:
                result.append(None)
        
        # Second pass: find yellows (wrong position)
        for i in range(WORD_LENGTH):
            if guess_chars[i] is not None:
                if guess_chars[i] in target_chars:
                    result[i] = LetterState.YELLOW
                    target_chars[target_chars.index(guess_chars[i])] = None
                else:
                    result[i] = LetterState.GREY
        
        return tuple(result)

    def make_guess(self, guess: Guess) -> GuessResult:
        """Submit a guess and update game state."""
        if self.game_over:
            raise ValueError("Game is already over")
        
        result = self.evaluate_guess(guess)
        self.guesses.append((guess, result))
        self.attempts_remaining -= 1
        
        # Check win condition
        if result == (LetterState.GREEN,) * WORD_LENGTH:
            self.game_won = True
            self.game_over = True
        elif self.attempts_remaining == 0:
            self.game_over = True
        
        return result

    def get_guesses(self) -> list[tuple[Guess, GuessResult]]:
        """Return all guesses made so far."""
        return self.guesses.copy()


class WordleGame:
    """Main game class that manages the Wordle game."""

    def __init__(self, words_file: str = 'src/config/data/words.txt') -> None:
        """Initialize the game by loading words and selecting a daily word."""
        self.words = load_words(words_file)
        self.game_state: Optional[GameState] = None

    def start_game(self) -> None:
        """Start a new game with a daily word."""
        target_word = get_daily_word(self.words)
        self.game_state = GameState(target_word)

    def make_guess(self, guess: Guess) -> GuessResult:
        """Submit a guess for the current game."""
        if self.game_state is None:
            raise ValueError("No game in progress")
        return self.game_state.make_guess(guess)

    def get_state(self) -> GameState:
        """Get the current game state."""
        if self.game_state is None:
            raise ValueError("No game in progress")
        return self.game_state

    def restart_game(self) -> None:
        """Restart the game with a new daily word."""
        self.start_game()

    def reveal_word(self) -> Word:
        """Reveal the target word (for end of game)."""
        if self.game_state is None:
            raise ValueError("No game in progress")
        return self.game_state.target_word
