# Baba is u limited Жaba edition with new level, textures, multiplayer, open-source, and best refactored code.
## Концепция

### Что это такое?
Наша игра является переделка другой зарубежной игры под названием Baba is you.

Вкратце, Baba is you - это видеоигра в жанре головоломки, где можно изменять правила уровня. 
В каждом уровне **правила представлены в виде блоков** которые можно передвигать и всячески взаимодействовать.

### Чем отличается от оригинала?
Есть немало пунктов, что добавляет наше DLC:
1. Она сделана в России
2. Она open-source
3. У неё заменены текстуры на более подходящие.
4. У неё есть мультиплеер на одном устройстве, и если хватит времени то и по сети
5. В ней больше уровней

## Интерфейс
### Главное меню
Главное меню должно выглядеть следующим образом:
![Главное меню](https://i.imgur.com/OGfpf6l.jpeg)
Жаба на главном меню находится под управлением игрока и передвигается только по кнопкам, если нажать на Enter, тогда кнопка нажмётся. 
Также не исключено использование мыши, с ней также можно нажимать на кнопки. 
В главном меню есть 7 кнопок:

 1. `Продолжить играть на n слоте`, если жаба находится на этой кнопке, тогда нажатием на w и s будет меняться слот игры с 1-3 включительно, и нажатием на пробел игра продолжится с сохранения на этом слоте, при этом если сохранения в игре не существует, тогда игра начнётся с самого 1-го уровня. Также, если наведена мышка на кнопку, тогда при колёсике мыши будет аналогично меняться слот, и при нажатии левой кнопкой мыши на неё будут такие же действия как и при нажатии на пробел, когда там находится жаба.
 2. `Чит-панель`, если жаба находится на этой кнопке и была нажат пробел, или она была кликнута мышью(далее это будет называться нажатие на кнопку), игра удаляет саму-себя. 
 3. `Редактор уровней`, это редактор уровней, в котором можно строить карту из блоков, выбирать спавн жабы, и прочее. Карту можно будет именовать, и сохранить в один файл, для передачи другим игрокам, и игры в неё в меню `Играть на других уровнях`.
 4. `Создатели`, если её нажали, жаба и меню начнут двигаться наверх, а снизу начнёт появляться список контрибьюторов репозитория игры, после конца титров, меню и жаба вернутся на своё место.
 5. `Играть на других уровнях`, при нажатии на неё, игра перейдёт в соответствующее меню.
 6. `Настройки`, при нажатии на неё, игра перейдёт в соответствующее меню.
 7. `Выйти из игры`, при нажатии на эту кнопку, игра выходит меньше чем за 1 секунду.
### Играть на других уровнях
![Меню выбора уровня](https://i.imgur.com/XC0extb.jpeg)
	 На данном меню жаба может выбирать карты нажатием на W и S, или прокрутом колёсика вперёд и назад, при нажатии на пробел, начнётся игра в карте рядом с которой будет жаба. Если кол-во карт больше 7 и не помещается на экран, тогда при попытке переместить жабу на 8-ю карту, 1-я карта выйдет из списка и появится 8-я карта снизу, тоже самое будет если переместить жабу с 8-й картой на 1-бю только наоборот. Если жаба находится в самом низу списка, тогда при попытке переместить её вниз, или нажатием на клавишу TAB в любом положении жабы, жаба переместится на кнопку "Назад", и если в таком положении переместить жабу наверх она окажется на последней карте в списке, и если нажать на эту кнопку, или нажать на клавишу ESC в не зависимости от расположения жабы, игра перейдёт на главное меню.
### Настройки
![Меню настроек](https://i.imgur.com/6c3793D.jpeg)
	На данном меню жаба может выбирать настройки, ползунки, и кнопку "Назад", нажатием на клавиши W и S. При нажатии на кнопку настройки, настройка станет активной, а кнопка изменит свой цвет на красный, и на ней появится галочка.
	Если жаба находится на ползунке, она может менять его громкость, нажатиями на клавиши A и D, а при нажатии на пробел, громкость на этом ползунке станет 0%, и при повторном нажатии, громкость на этом ползунке станет 100%.
	Также, громкость на ползунках можно менять, зажимая мышью ползунок и ведя его влево-вправо.
	При нажатии на кнопку "Назад", игра вернётся на главное меню.
	А при нажатии на кнопку `Настройки языка`, появится следующее подменю:
#### Настройки языка
![Настройки языка](https://i.imgur.com/cLMDIPk.jpeg)
	В нём будет два(или больше) языка, и кнопка "Назад". Жаба может передвигаться между кнопками нажатиями на WASD, выбрать язык можно нажатием на Пробел, и язык сменится тут же.
	При нажатии на кнопку "Назад", игра перемещается на меню "Настройки".
## Техническая часть
### Архитектура приложения
#### Шаблон проектирования
Игра должна использовать [шаблон проектирования "стратегия"](https://en.wikipedia.org/wiki/Strategy_pattern) как основу.
##### Плюсы
- Удобное переключение между меню игры.
- [Меньше повторений кода](https://ru.wikipedia.org/w/index.php?title=Don%E2%80%99t_repeat_yourself&stable=1)
##### Минусы
- Большее количество [классов](https://bit.ly/3uMPiTw). 
#### Основные Классы
##### GameContext
Основной класс игры вокруг которого всё будет крутиться.
##### GameStrategy
[Абстрактный базовый класс](https://bit.ly/3sBzdNI) (интерфейс) необходимый для определения отрисовки меню в GameContext. Его [метод](https://bit.ly/3rJrxtR) draw принимает в себя [список](https://bit.ly/3gDYHo7) [событий](https://www.pygame.org/docs/ref/event.html#pygame.event.EventType), и время прошедшее между кадрами для не зависимого от [количества кадров в секунду](https://bit.ly/33fupoF), движения, а возвращает структуру State.
##### GameState
Является перечислением изменений в GameContext, например возврат на прошлый GameStrategy, остановка игры, сменить GameStrategy на другой, и т.д
##### State
Является структурой хранящий дополнительную информацию для GameState, например какой GameStraregy необходимо сменить. Необходим просто для замены кортежа.
##### Button
Является [классом](https://bit.ly/3uMPiTw) кнопки, необходимом для удобного их создания. Имеет [методы](https://bit.ly/3rJrxtR):
- draw, метод отрисовки, принимающий [surface](https://www.pygame.org/docs/ref/surface.html#pygame.Surface) на котором будет происходить отрисовка кнопки.
- update, метод обновления, принимающий [список](https://bit.ly/3gDYHo7) [событий](https://www.pygame.org/docs/ref/event.html#pygame.event.EventType).
##### SpriteManager
Является [классом](https://bit.ly/3uMPiTw), необходимым для установки и кеширования спрайтов
#### Структура файлов
##### classes/
В директории classes/ должны находиться [py файлы](https://ru.wikipedia.org/wiki/Python), в которых хранится не больше одного [класса](https://bit.ly/3uMPiTw). 
##### elements/
В директории elements/ должны находиться [py файлы](https://ru.wikipedia.org/wiki/Python), в которых хранится не больше одного [класса](https://bit.ly/3uMPiTw), реализующего [Абстрактный базовый класс](https://bit.ly/3sBzdNI) GameStrategy.
##### sprites/
В директории sprites/ должны находиться спрайты игры, типа [WebP](https://ru.wikipedia.org/wiki/WebP) с [альфа-каналом](https://bit.ly/3GJr7HV), сгруппированные по директориям, пример: `"sprites/keke/0_1.png, sprites/keke/0_2.png, ..., sprites/baba/0_1.png, sprites/baba/0_2.png, и т.д.`.
