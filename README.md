# ElaChess

ElaChess is a chess engine built entirely from scratch in Python.

The project is an ongoing exploration of the algorithms and techniques behind modern chess engines. New features, algorithms, and optimisations are continuously added as ElaChess evolves and becomes stronger.

**Current version:** `v0.5`


## Features

### Board Representation
- Mailbox board representation (0x88)
- Piece lists

### Move Generation
- Pseudo-legal move generation

### Search
- Alpha-Beta pruning
- Iterative deepening
- Transposition table
- Quiescence search

### Evaluation
- Simplified evaluation function
  - Material evaluation
  - Piece-square tables

### Interface
- Universal Chess Interface (UCI)
- Command-line interface (CLI)


## Strength

ElaChess is currently rated on Lichess across multiple time controls:

| Time Control | Rating |
|--------------|--------|
| Bullet       | 1558   |
| Blitz        | 1456   |
| Rapid        | 1600   |
| Classical    | 1698   |

These ratings are based on games played by ElaChess on Lichess and may change as more games are played.


## Getting Started

### Requirements
- Git
- Python 3.10 or later

### Download

Clone the repository:

```bash
git clone https://github.com/itsdaveba/ela-chess.git
cd ela-chess
```

### Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` includes PyInstaller, which is used to build the standalone executable.

### Command-Line Interface

ElaChess includes a command-line interface for playing directly from the terminal.

To see the available options:

```bash
python play.py -h
```

### Build

Build ElaChess with:

```bash
pyinstaller uci.py -n ela-chess -F
```

The executable will be created in the `dist` directory:

```text
dist/
└── ela-chess.exe
```

### Run

```bash
./dist/ela-chess
```

ElaChess communicates using the Universal Chess Interface (UCI) and can be used with any chess GUI that supports UCI engines.

### Using a Chess GUI

To play against ElaChess:

1. Build the engine using the command above.
2. Locate the executable in the `dist` directory.
3. Open your preferred chess GUI.
4. Add the ElaChess executable as a new UCI engine.
5. Start a game against ElaChess.


## Roadmap

ElaChess is actively under development. The current focus is on improving search, evaluation, move ordering, and overall playing strength.

Planned improvements include:

- Bitboards
- Improved evaluation function
- Move ordering
- Aspiration windows
- Improved time management
- Opening book
- Endgame tablebases
- C implementation

## License

ElaChess is released under the `MIT License`.

See the [LICENSE](LICENSE) file for the full license text.