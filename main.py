import argparse

import settings
from elements.main_menu import main_menu


def main():
    parser = argparse.ArgumentParser(description='Jaba')
    parser.add_argument("-d", "--debug",        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.debug:
        settings.instant_win = 1
        print("Instant win on")


if __name__ == '__main__':
    main()
    main_menu()
