### [Русский вариант тут!](README-ru.md)

# The original game is called [Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) 
We don't take any credit for creating the game's idea, mechanics, sprites, and/or music. This is a project created for educational purposes with consent of the original game's creator ([Hempuli](https://www.hempuli.com)) via email.

## This project is a "Baba is You" clone written in python using the pygame library

## Concept

Baba is you is a puzzle videogame, where you have ability to change the game's rules. 
In each level **the rules are represented with blocks** which you can move and interact with.

## How to launch
```sh
git clone https://github.com/Danilado/jaba-is-you.git
cd ./jaba-is-you
pip install .
python main.py
```

### Profiling
```sh
# Set the FPS to 200+ in settings.py
pip install snakeviz
python profiler.py
# Play the game normally to collect data
snakeviz main.profile
```
