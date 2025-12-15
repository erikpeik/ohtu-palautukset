# Testing Guide

## Running Tests

This project includes comprehensive automated tests for the web application.

### Prerequisites

Tests are automatically configured when you install the project dependencies:

```bash
poetry install
```

### Running All Tests

To run all tests:

```bash
poetry run pytest src/tests/
```

### Running Tests with Verbose Output

To see detailed test names and results:

```bash
poetry run pytest src/tests/ -v
```

### Running Tests with Coverage

To see code coverage:

```bash
poetry run pytest src/tests/ --cov=src --cov-report=term-missing
```

## Test Coverage

The test suite includes 33 tests covering:

- **Index Route Tests**: Main page loading and game mode selection
- **Start Game Tests**: Game initialization for all three modes (Player vs Player, Player vs AI, Player vs Improved AI)
- **Play Game Tests**: Game interface display and score tracking
- **Make Move Tests**:
  - All rock-paper-scissors game logic
  - Player vs Player moves
  - Simple AI behavior
  - Improved AI with memory
  - Invalid move handling
- **Round Result Tests**: Result display and winner determination
- **Game Over Tests**: Final score display and session cleanup
- **Win Logic Tests**: All winning combinations for rock-paper-scissors
- **Game Flow Tests**: Complete multi-round game scenarios

Current coverage: **88%** for web_app.py

## Test Structure

```
src/tests/
├── __init__.py
└── test_web_app.py  # Main test file with all web application tests
```

## Test Classes

- `TestIndexRoute`: Tests for the main landing page
- `TestStartGame`: Tests for game initialization
- `TestPlayGame`: Tests for game display
- `TestMakeMove`: Tests for move processing and game logic
- `TestRoundResult`: Tests for round result display
- `TestGameOver`: Tests for game completion
- `TestWinLogic`: Tests for win/loss/tie logic
- `TestGameFlow`: Integration tests for complete game flows
