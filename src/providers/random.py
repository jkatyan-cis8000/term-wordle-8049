"""Random number provider for the Wordle game."""

import random


class RandomProvider:
    """Provider for random number generation."""

    def __init__(self) -> None:
        """Initialize the random provider."""
        self._seeded = False
        self._seed_value = 0

    def seed(self, value: int) -> None:
        """Set a seed for deterministic randomness."""
        random.seed(value)
        self._seeded = True
        self._seed_value = value

    def reset_seed(self) -> None:
        """Reset to non-deterministic randomness."""
        random.seed()
        self._seeded = False
        self._seed_value = 0

    def randint(self, low: int, high: int) -> int:
        """Generate a random integer in [low, high]."""
        return random.randint(low, high)

    def choice(self, items: list) -> object:
        """Choose a random item from a list."""
        return random.choice(items)


# Global instance for use across the application
_random_provider = RandomProvider()


def seed(value: int) -> None:
    """Set a seed for deterministic randomness."""
    _random_provider.seed(value)


def reset_seed() -> None:
    """Reset to non-deterministic randomness."""
    _random_provider.reset_seed()


def randint(low: int, high: int) -> int:
    """Generate a random integer in [low, high]."""
    return _random_provider.randint(low, high)


def choice(items: list) -> object:
    """Choose a random item from a list."""
    return _random_provider.choice(items)
