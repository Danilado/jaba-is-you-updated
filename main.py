import argparse

import settings
from classes.game_context import GameContext
from elements.global_classes import sprite_manager, sound_manager
from elements.main_menu import MainMenu


def main():
    parser = argparse.ArgumentParser(description='Jaba')
    parser.add_argument("-d", "--debug",
                        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.debug:
        settings.DEBUG = True
        print("Debug on")

    sound_manager.start_download()


if __name__ == '__main__':
    main()
    GameContext(MainMenu).run()
