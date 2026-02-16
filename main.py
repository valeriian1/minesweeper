import argparse
from src.game import Game

def main():
    parser = argparse.ArgumentParser(description="Minesweeper Game")
    parser.add_argument(
        '--difficulty', '-d', 
        type=str, 
        choices=['easy', 'medium', 'hard'], 
        default='easy',
        help="Set the difficulty level (easy, medium, hard)"
    )
    args = parser.parse_args()

    minesweeper = Game(difficulty=args.difficulty)
    minesweeper.run()

if __name__ == "__main__":
    main()
