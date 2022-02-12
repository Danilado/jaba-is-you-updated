import argparse

import settings
from classes.game_context import GameContext
from elements.main_menu import MainMenu


def main():
    parser = argparse.ArgumentParser(description='Jaba')
    parser.add_argument("-d", "--debug",        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.debug:
        settings.DEBUG = 1
        print("Debug on")


if __name__ == '__main__':
    main()
    GameContext(MainMenu).run()
