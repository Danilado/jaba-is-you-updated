import threading
from random import choice
from typing import Optional, TYPE_CHECKING, Sequence, Set, List, Callable

from classes.objects import Object
from classes.particle import Particle, ParticleStrategy
from classes.text_rule import TextRule
from elements.global_classes import sprite_manager
from global_types import COLOR

if TYPE_CHECKING:
    from elements.play_level import PlayLevel


class ParticleMover:
    """
    Класс двигающий партиклы
    """
    def __init__(self, x_offset: Sequence[int], y_offset: Sequence[int], size: Sequence[int],
                 max_rotation: Sequence[int], wait_delay: float, duration: float,
                 count: Optional[Sequence[int]] = None):
        """
        Конструктор класса

        :param x_offset: Диапазон чисел в котором случайно будет выбираться отступ для партикла по оси x
        :param y_offset: Диапазон чисел в котором случайно будет выбираться отступ для партикла по оси y
        :param size: Диапазон чисел в котором случайно будет выбираться размер для партикла
        :param max_rotation: Диапазон чисел в котором случайно будет выбираться градус поворота в конце анимации
        :param wait_delay: Число, обозначающее задержку между созданием партиклов
        :param duration: Длительность партикла
        :param count: Диапазон чисел в котором случайно будет выбираться количество частиц за раз
        """
        self.count = count if count is not None else range(1, 4)
        self.wait_delay: float = wait_delay
        self.duration: float = duration
        self._stop_event = threading.Event()
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.size = size
        self.max_rotation = max_rotation
        self._level_processor: Optional["PlayLevel"] = None
        self._rule_objects: Set[Object] = set()
        self._thread: Optional[threading.Thread] = None
        self._force_sprite_color: Optional[COLOR] = None

    def for_rule_objects(self, func: Callable):
        for rule in self._rule_objects:
            func(rule)

    def update_on_apply(self, level_processor: "PlayLevel", rule_object: Object, color: str,
                        particle_sprite_name: str = ""):
        """
        Инкапсуляция :attr:`~.RuleObjectParticleHelper.rule_object` и :attr:`~.RuleObjectParticleHelper.level_processor`
        То есть устанавливает их.

        :param level_processor: Обработчик уровня
        :param rule_object: Объект к которому применяются партиклы
        :param color: Объект из которого необходимо брать цвет
        :param particle_sprite_name: Название спрайта для партикла
        :return: Ничего
        """
        if level_processor != self._level_processor:
            self._rule_objects.clear()
        self._level_processor = level_processor
        have_rule_object = False
        for rule in self._rule_objects:
            if repr(rule) == repr(rule_object):
                have_rule_object = True
                break
        if not have_rule_object:
            self._rule_objects.add(rule_object)
        palette_pixel_position = sprite_manager.default_colors[color]
        self._force_sprite_color = self._level_processor.current_palette.pixels[
            palette_pixel_position[1]][palette_pixel_position[0]]
        if not self.started:
            self.start(particle_sprite_name)

    def update_on_rules_changed(self, new_rules: List[TextRule], rule_name: str):
        need_to_stop = True
        for rule in new_rules:
            rule_end = f' is {rule_name}'
            if rule_end in rule.text_rule and rule.text_rule[:rule.text_rule.index(rule_end)] in \
                    [i.name for i in self._rule_objects]:
                need_to_stop = False
        if self.started and need_to_stop:
            self.stop()
            return False
        return True

    def stop(self):
        """
        Посылает запрос на остановку потока(изменения частицы)

        :raises RuntimeError: Если что-то пошло не так, например поток уже остановлен или не запущен
        :raises ChildProcessError: Если поток не может(или не хочет) остановиться за 5 секунд.
        :return: Ничего
        """
        if not self.started:
            raise RuntimeError("Thread already stopped or didn't started")
        self._stop_event.set()
        self._thread.join(5)
        if self._thread.is_alive():
            raise ChildProcessError("Can't join thread. Thread is dead or frozen")
        self._rule_objects.clear()

    def start(self, particle_sprite_name: str = ""):
        """
        Запускает поток
        :return: Ничего
        """
        thread = threading.Thread(target=self._thread_work, args=(particle_sprite_name,), daemon=True)
        self._stop_event.clear()
        thread.start()
        self._thread = thread

    @property
    def started(self) -> bool:
        """
        .. getter: Возвращает bool, означающий запущен ли поток или нет

        .. setter:
            Нету.
            Используйте :meth:`~.RuleObjectParticleHelper.start` для запуска
            или :meth:`~.RuleObjectParticleHelper.stop` для остановки
        """
        return self._thread.is_alive() if self._thread is not None else False

    def _thread_work_one_particle(self, rule_object: Object, particle_sprite_name: str):
        if self._level_processor is None:
            raise RuntimeError("self._level_processor is not initialized")
        for _ in range(choice(self.count)):
            x_offset = choice(self.x_offset)
            y_offset = choice(self.y_offset)
            size = choice(self.size)
            max_rotation = choice(self.max_rotation)
            color: COLOR
            if self._force_sprite_color is None:
                palette_pixel_position = sprite_manager.default_colors[rule_object.name]
                color = self._level_processor.current_palette.pixels[
                    palette_pixel_position[1]][
                    palette_pixel_position[0]]
            else:
                color = self._force_sprite_color
            self._level_processor.particles.append(Particle(particle_sprite_name, ParticleStrategy(
                (rule_object.xpx, rule_object.xpx + x_offset),
                (rule_object.ypx, rule_object.ypx + y_offset),
                (size, size),
                (0, max_rotation), 10,
                self.duration,
                randomize_start_values=True
            ), color))

    def _thread_work(self, particle_sprite_name: str):
        while not self._stop_event.is_set():

            rule_objects = self._rule_objects.copy()
            # Нужно чтобы если другой поток поменял _rule_objects цикл не вылетел

            for rule_object in rule_objects:
                self._thread_work_one_particle(rule_object, particle_sprite_name)
            self._stop_event.wait(self.wait_delay)

    def __del__(self):
        if self.started:
            self.stop()
