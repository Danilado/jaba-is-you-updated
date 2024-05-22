# The final project for the "Industrial Programming" course of [MSHP](https://informatics.ru)

# The original game is called [Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) 
We don't take any credit on creating the game idea and /or mechanics. This is a project created for educational purposes with consent of original game's creator (Hempuli) through an email

## This project is a "baba is you" clone written in python using the pygame library

## Concept

Baba is you is a puzzle videogame, where you have ability to change the game's rules. 
In each level **the rules are represented with blocks** which you can move and interact with.

## How to launch
```sh
git clone https://github.com/Danilado/jaba-is-you.git
cd ./jaba-is-you
pip install -r requirements.txt
pip install -v -e .
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
