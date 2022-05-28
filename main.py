import argparse

import settings
from classes.game_context import GameContext
from elements.global_classes import sound_manager
from elements.progressbar_menu import ProgressBarMenu


def main():
    parser = argparse.ArgumentParser(description='Jaba')
    parser.add_argument("-d", "--debug", help='Logs some useful information', action="store_true")
    args = parser.parse_args()
    if args.debug:
        settings.DEBUG = True
        print("Debug on")
        print("Какой дебаг? Багов не бывает.")

    sound_manager.start_download()


if __name__ == '__main__':
    try:
        main()
        GameContext(ProgressBarMenu).run()
    except:
        print("Возникла страшная критическая ошибка, но мы будем делать вид, что нет")
