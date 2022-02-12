import time
from functools import partial
import pygame
import os

from elements.global_classes import EuiSettings, IuiSettings
from classes.button import Button
from elements.objects import Object
import settings

left: bool = False
tool = 1
direction = 0
is_text = False
name = None


def my_deepcopy(arr):
    new_arr = []
    for val in arr:
        if isinstance(val, list):
            new_arr.append(my_deepcopy(val))
        else:
            new_arr.append(val)
    return new_arr


def unparse_all(state):
    s = ''
    for row in state:
        for cell in row:
            for object in cell:
                s += object.unparse() + '\n'
    return s


def save(state):
    with open(f"levels/level{len(os.listdir('levels/'))}.omegapog_map_file_type_MLG_1337_228_100500_69_420", 'w',
              encoding='utf-8') as file:
        file.write(unparse_all(state))


def set_name(string):
    global name
    name = string


def turn(dir):
    global direction  # 1     :   clockwise (Hotkey - E)
    direction = (direction + dir) % 4  # -1    :   counter-clockwise (Hotkey - Q)


def set_tool(string):
    global tool  # 1     :   Create (Hotkey - C)
    tool = string  # 0     :   Delete (Hotkey - X)


def is_text_swap():
    global is_text  # 1 :   text     (Hotkey - T)
    is_text = False if is_text else True  # 2 :   not text (Hotkey - T)


def edit():
    text_color = (200,) * 3
    text_font = pygame.font.SysFont("segoeuisemibold", 32)
    changes = []
    current_state = [[[] for i in range(32)] for j in range(18)]
    try:
        #   Button(x, y, width, height, outline, settings, text="", action=None)
        buttons = [
            Button(settings.RESOLUTION[0] + 17, 25, 75, 75, (0, 0, 0), EuiSettings(), "JA\nBA",
                   partial(set_name, "jaba")),
            Button(settings.RESOLUTION[0] + 101, 25, 75, 75, (0, 0, 0), EuiSettings(), "RO\nCK",
                   partial(set_name, "rock")),
        ]
        main_screen = pygame.display.set_mode((1800, 900))
        clock = pygame.time.Clock()
        timeout = 0
        focus = (-1, -1)
        while not left:
            indicators = [
                Button(settings.RESOLUTION[0] + 17, settings.RESOLUTION[1] - 192, 75, 75, (0, 0, 0), IuiSettings(),
                       f"Obj\n{name}"),
                Button(settings.RESOLUTION[0] + 101, settings.RESOLUTION[1] - 192, 75, 75, (0, 0, 0), IuiSettings(),
                       f"Text\n{'True' if is_text == 1 else 'False'}", is_text_swap),
                Button(settings.RESOLUTION[0] + 17, settings.RESOLUTION[1] - 100, 75, 75, (0, 0, 0), IuiSettings(),
                       f"Tool\n{'Create' if tool == 1 else 'Delete' if tool == 0 else 'Lookup'}",
                       partial(set_tool, 0 if tool == 1 else 1 if tool == 2 else 2)),
                Button(settings.RESOLUTION[0] + 101, settings.RESOLUTION[1] - 100, 75, 75, (0, 0, 0), IuiSettings(),
                       f"Dir\n{'↑' if direction == 0 else '→' if direction == 1 else '↓' if direction == 2 else '←'}",
                       partial(turn, 1)),
            ]

            timeout += 1
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    save(current_state)
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_screen = pygame.display.set_mode((1600, 900))
                        main_screen.fill((0, 0, 0))
                        save(current_state)
                        return
                    if event.key == pygame.K_e:
                        turn(1)
                    if event.key == pygame.K_q:
                        turn(-1)
                    if event.key == pygame.K_t:
                        is_text_swap()
                    if event.key == pygame.K_c:
                        set_tool(1)
                    if event.key == pygame.K_x:
                        set_tool(0)
                    if event.key == pygame.K_a:
                        set_tool(2)
                    if event.key == pygame.K_z and event.mod == 4160:
                        if len(changes) != 0:
                            print(current_state == changes[-1])
                            current_state = changes[-1]
                            changes.pop()
                    if settings.DEBUG:
                        print(f"""
event: KeyDown -> {event.unicode} mod {event.mod}

focus position: {focus[0]} {focus[1]}
tool:           {tool}
direction:      {direction}
is_text:        {is_text}
name:           {name}

                        """)
                if event.type == pygame.MOUSEMOTION:
                    if event.pos[0] <= 1600:
                        focus = (event.pos[0] // 50, event.pos[1] // 50)
                    else:
                        focus = (-1, -1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if focus[0] != -1 and focus[1] != -1:
                        flag = 0
                        if tool == 1 and name != None:
                            for object in current_state[focus[1]][focus[0]]:
                                if object.name == name:
                                    flag = 1
                                    break
                            if not flag:
                                changes.append(my_deepcopy(current_state))
                                current_state[focus[1]][focus[0]].append(
                                    Object(focus[0], focus[1], direction, name, None, is_text))
                        elif tool == 0:
                            if len(current_state[focus[1]][focus[0]]) > 0:
                                changes.append(my_deepcopy(current_state))
                                current_state[focus[1]][focus[0]].pop()
                        else:
                            print(current_state[focus[1]][focus[0]])
                    if settings.DEBUG:
                        print(f"""
event: MouseDown

focus position: {focus[0]} {focus[1]}
tool:           {tool}
direction:      {direction}
is_text:        {is_text}
name:           {name}

                        """)

            if left:
                break

            for button in buttons:  # Передать кнопкам события кликов
                if not left and button.update(events) and button.action is exit:
                    break
            for indicator in indicators:
                if not left and indicator.update(events) and button.action is exit:
                    break

            main_screen.fill((0, 0, 0))

            for button in buttons:  # Отрисовать кнопки
                button.draw(main_screen)
            for indicator in indicators:
                indicator.draw(main_screen)

            pygame.draw.rect(main_screen, (44, 44, 44), (focus[0] * 50, focus[1] * 50, 50, 50))

            for i in range(settings.RESOLUTION[0] // 50 + 1):  # Отрисовать сетку
                pygame.draw.line(main_screen, (255, 255, 255), (i * 50, 0), (i * 50, settings.RESOLUTION[1]), 1)
            for i in range(settings.RESOLUTION[1] // 50 + 1):
                pygame.draw.line(main_screen, (255, 255, 255), (0, i * 50 - (1 if i == 18 else 0)),
                                 (settings.RESOLUTION[0], i * 50 - (1 if i == 18 else 0)), 1)

            for row in current_state:
                for cell in row:
                    for object in cell:
                        object.draw(main_screen)

            pygame.display.flip()
            clock.tick(60)
            pygame.time.wait(60)
        pygame.quit()
    except KeyboardInterrupt:
        save(current_state)
        pass
