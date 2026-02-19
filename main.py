import argparse
from src.engine.game import Game
from src.utils.constants import DIFFICULTIES

def main():
    parser = argparse.ArgumentParser(description="Minesweeper Game")
    parser.add_argument(
        '--difficulty', '-d', 
        type=str, 
        choices=list(DIFFICULTIES.keys()),
        default='easy',
        help=f"Set the difficulty level ({', '.join(DIFFICULTIES.keys())})"
    )
    args = parser.parse_args()

    minesweeper = Game(difficulty=args.difficulty)
    minesweeper.run()

if __name__ == "__main__":
    main()
