### [Русский вариант тут!](README-ru.md)

# The original game is called [Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) 
We don't take any credit for creating the game's idea, mechanics, sprites, and/or music. This is a project created for educational purposes with consent of the original game's creator ([Hempuli](https://www.hempuli.com)) via email.

## This project is a "Baba is You" clone written in python using the pygame library

## Concept

Baba is you is a puzzle videogame, where you have ability to change the game's rules. 
In each level **the rules are represented with blocks** which you can move and interact with.

## How to launch

There are two ways: from source and from a binary file.
To install from source, you need Python 3.8+. For a binary file you need amd64 Linux or Windows.

### From source
```sh
git clone https://github.com/Danilado/jaba-is-you.git
cd ./jaba-is-you
pip install .
python main.py
```

### From binary files
Go to [GitHub Releases](https://github.com/Danilado/jaba-is-you/releases) and download the archive you need. 
Unpack it and run the executable file. 

---

### Profiling
```sh
# Set the FPS to 200+ in settings.py
pip install snakeviz
python profiler.py
# Play the game normally to collect data
snakeviz main.profile
```
