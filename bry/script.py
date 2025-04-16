from browser import document

from sub_classes import *
from algorithms import *


class App:
    """Основной класс приложения для генерации и визуализации лабиринтов.

    Attributes:
        width (int): Ширина лабиринта в клетках.
        height (int): Высота лабиринта в клетках.
        cell_size (Tuple[int, int]): Размер клетки в пикселях (width, height).
        algorithms (List[callable]): Доступные алгоритмы генерации лабиринтов.
        algorithm_indx (int): Индекс текущего алгоритма.
        algorithm (callable): Текущий выбранный алгоритм генерации.
        maze (Maze): Экземпляр класса лабиринта.
        canvas: HTML canvas элемент для отрисовки.
        width_inp: Поле ввода ширины лабиринта.
        height_inp: Поле ввода высоты лабиринта.
        algorithm_inp: Выпадающий список выбора алгоритма.
        ctx: Контекст рисования canvas.
    """

    def __init__(self) -> None:
        """Инициализирует приложение, настраивает элементы интерфейса и начальные параметры."""
        self.__brython_init()  # Инициализация Brython элементов
        self.__size_init(1, 1)  # Установка начального размера
        
        # Настройка алгоритмов генерации
        self.algorithms = [
            AldousBroder(self), 
            BinaryTree(self), 
            Sidewinder(self)
        ]
        self.algorithm_indx = 0
        self.algorithm = self.algorithms[self.algorithm_indx]
        self.maze = Maze(self)  # Создание экземпляра лабиринта

    def __size_init(self, width: int, height: int) -> None:
        """Инициализирует размеры лабиринта и вычисляет размер клеток.
        
        Args:
            width (int): Ширина лабиринта в клетках.
            height (int): Высота лабиринта в клетках.
        """
        self.width = width
        self.height = height
        self.cell_size = (self.canvas.width / self.width, self.canvas.height / self.height)

    def __brython_init(self) -> None:
        """Инициализирует Brython-специфичные элементы DOM и привязывает события."""
        self.canvas = document['myCanvas']
        self.width_inp = document['myWidth']
        self.height_inp = document['myHeight']
        self.algorithm_inp = document['myAlgorithm']

        self.ctx = self.canvas.getContext("2d")
        document["myButton"].bind("click", self.__generate)

    def __generate(self, _) -> None:
        """Обработчик события генерации лабиринта."""
        if self.width_inp.value and self.height_inp.value:
            self.__size_init(int(self.width_inp.value), int(self.height_inp.value))

        self.algorithm_indx = int(self.algorithm_inp.value)
        self.algorithm = self.algorithms[self.algorithm_indx]
        self.maze.clear()  # Очистка предыдущего лабиринта
        self.algorithm.create_maze()  # Генерация нового лабиринта
        self.__draw()  # Отрисовка

    def __draw(self) -> None:
        """Отрисовывает лабиринт на canvas."""
        ctx = self.ctx

        # Очистка canvas
        ctx.beginPath()
        ctx.rect(0, 0, self.canvas.width, self.canvas.height, 1)
        ctx.fillStyle = "#0a0a0a"  # Темно-серый фон
        ctx.fill()
        ctx.closePath()

        # Отрисовка горизонтальных стен
        for i in range(self.height - 1):
            for j in range(self.width):
                if self.maze.horisontal_walls[i][j]:
                    ctx.beginPath()
                    ctx.rect(
                        j * self.cell_size[0], 
                        (i + 1) * self.cell_size[1], 
                        self.cell_size[0], 
                        1 
                    )
                    ctx.fillStyle = "#FFFFFF"  
                    ctx.fill()
                    ctx.closePath()

        # Отрисовка вертикальных стен
        for i in range(self.height):
            for j in range(self.width - 1):
                if self.maze.vertical_walls[i][j]:
                    ctx.beginPath()
                    ctx.rect(
                        (j + 1) * self.cell_size[0], 
                        i * self.cell_size[1], 
                        1, 
                        self.cell_size[1]
                    )
                    ctx.fillStyle = "#FFFFFF" 
                    ctx.fill()
                    ctx.closePath()


# Создание и запуск приложения
app = App()
