### [Русский вариант тут!](#ru)


<a id="en"></a>
# The final project for the "Industrial Programming" course of [MSHP](https://informatics.ru)

# The original game is called [Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) 
We don't take any credit for creating the game's idea, mechanics, sprites, and/or music. This is a project created for educational purposes with consent of the original game's creator ([Hempuli](https://www.hempuli.com)) via email.

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

<a id="ru"></a>

# Итоговый проект для курса "Промышленное программирование" [МШП](https://informatics.ru)

# Оригинальная игра называется [Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) 
Мы не пытаемся выдать себя за авторов идеи, механик, спрайтов, и/или музыки игры. Это - проект, созданный в образовательных целях с согласия разработчика оригинальной игры ([Hempuli](https://www.hempuli.com)), полученного по электронной почте.

## Проект представляет из себя клон игры "baba is you", написанный на python с применением библиотеки pygame

## Концепт

Baba is you - это видеоигра в жанре "головоломки", где у игрока есть возможность менять правила самой игры. 
В каждом уровне, **правила представлены в виде блоков**, которые можно передвигать, или взаимодействовать с ними другими способами.

## Как запускать
```sh
git clone https://github.com/Danilado/jaba-is-you.git
cd ./jaba-is-you
pip install -r requirements.txt
pip install -v -e .
python main.py
```

### Профилирование
```sh
# Установите значение FPS на 200 или более в файле settings.py
pip install snakeviz
python profiler.py
# Играйте в игру, чтобы собрать данные
snakeviz main.profile
```