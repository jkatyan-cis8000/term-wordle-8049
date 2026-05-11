"""Application runtime for the Wordle game.

This module provides the core orchestration logic for the application.
It does not directly import ui modules to respect layer constraints.

To run the application:
    python -m src.ui.cli
"""

import sys


def entry_point() -> int:
    """Core entry point that orchestrates the application.

    Due to layer constraints (runtime cannot import ui),
    the CLI is the entry point. This function exists to
    document the intended orchestration flow.
    """
    # This module demonstrates the intended entry point structure
    # In practice, run with: python -m src.ui.cli
    return 0


def run() -> int:
    """Run the application with default settings."""
    return entry_point()


if __name__ == '__main__':
    # Direct entry from runtime module
    sys.exit(run())
