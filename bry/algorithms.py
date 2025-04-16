from random import choice, randint, random
from script import App

from typing import List, Tuple


def check_cell(app: 'App', x: int, y: int) -> List[Tuple[int, int]]:
    """Проверяет соседние клетки на валидность и возвращает список доступных соседей.
    
    Args:
        app (App): Экземпляр главного приложения с параметрами лабиринта.
        x (int): x координата текущей клетки.
        y (int): y координата текущей клетки.
        
    Returns:
        valid_cells (List[Tuple[int, int]]): Список кортежей с координатами (x, y) доступных соседних клеток.
    """
    sub_list = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]  # Верх, низ, лево, право
    res = []
    for i, j in sub_list:
        if (i >= 0) and (j >= 0) and (i < app.width) and (j < app.height):
            res.append((i, j))
    return res


class AldousBroder:
    """Реализует алгоритм генерации лабиринта Aldous-Broder."""
    
    def __init__(self, app):
        """Инициализирует алгоритм с привязкой к главному приложению.
        
        Args:
            app (App): Экземпляр главного приложения.
        """
        self.app = app
        self.is_blank = True  # Флаг для инициализации пустого лабиринта
    
    def create_maze(self):
        """Генерирует лабиринт с использованием алгоритма Aldous-Broder.
        
        Алгоритм:
        1. Начинает со случайной клетки
        2. Случайно перемещается по соседним клеткам
        3. При посещении новой клетки убирает стену
        4. Продолжает пока не посетит все клетки
        """
        # Матрица посещенных клеток
        map = [[0 for _ in range(self.app.width)] for _ in range(self.app.height)]
        count = self.app.width * self.app.height - 1  # Количество непосещенных клеток
        
        # Начальная позиция
        x, y = randint(0, self.app.width - 1), randint(0, self.app.height - 1)
        map[y][x] = 1
        
        while count:
            sub_list = check_cell(self.app, x, y)
            i, j = choice(sub_list)  # Случайный сосед
            
            if not map[j][i]:  # Если клетка не посещена
                count -= 1
                map[j][i] = 1
                self.__del_wall(x, y, i, j)  # Удаляем стену между клетками
            
            x, y = i, j  # Перемещаемся в соседнюю клетку
            
    def __del_wall(self, x1: int, y1: int, x2: int, y2: int):
        """Удаляет стену между двумя соседними клетками.
        
        Args:
            (x1, y1): Координаты первой клетки.
            (x2, y2): Координаты второй клетки.
        """
        if x1 == x2:  # Вертикальные соседи - удаляем горизонтальную стену
            self.app.maze.horisontal_walls[min(y1, y2)][x1] = 0
        else:  # Горизонтальные соседи - удаляем вертикальную стену
            self.app.maze.vertical_walls[y1][min(x1, x2)] = 0


class BinaryTree:
    """Реализует алгоритм генерации лабиринта Binary Tree."""
    
    def __init__(self, app):
        """Инициализирует алгоритм с привязкой к главному приложению.
        
        Args:
            app (App): Экземпляр главного приложения.
        """
        self.app = app
        self.is_blank = True
    
    def create_maze(self):
        """Генерирует лабиринт с использованием алгоритма Binary Tree.
        
        Алгоритм:
        1. Проходит по всем клеткам (кроме граничных)
        2. Для каждой клетки случайно выбирает:
           - Удаление верхней стены (50% chance)
           - Удаление левой стены (50% chance)
        3. Обрабатывает граничные случаи
        """
        for depth in range(1, self.app.height):
            for i in range(self.app.width - 1):
                if random() <= 0.5:  # 50% chance
                    self.app.maze.vertical_walls[depth][i] = 0  # Удаляем левую стену
                else:
                    self.app.maze.horisontal_walls[depth - 1][i] = 0  # Удаляем верхнюю стену
        
        # Обработка границ
        for i in range(self.app.width - 1):
            self.app.maze.vertical_walls[0][i] = 0  # Удаляем все левые стены в первом ряду
        
        for j in range(self.app.height - 1):
            self.app.maze.horisontal_walls[j][-1] = 0  # Удаляем все верхние стены в последнем столбце


class Sidewinder:
    """Реализует алгоритм генерации лабиринта Sidewinder."""
    
    def __init__(self, app):
        """Инициализирует алгоритм с привязкой к главному приложению.
        
        Args:
            app (App): Экземпляр главного приложения.
        """
        self.app = app
        self.is_blank = True
    
    def create_maze(self):
        """Генерирует лабиринт с использованием алгоритма Sidewinder.
        
        Алгоритм:
        1. Проходит по рядам сверху вниз
        2. В каждом ряду собирает "набор" клеток
        3. Случайно выбирает момент соединения с верхним рядом
        4. С вероятностью 50% продолжает набор или соединяет его
        """
        for depth in range(1, self.app.height):
            sub_set = [0]  # Начальный набор клеток
            curr = 0  # Текущая позиция в ряду
            
            while curr < self.app.width:
                if (random() <= 0.5) or (curr == self.app.width - 1):
                    # Соединяем случайную клетку из набора с верхним рядом
                    self.app.maze.horisontal_walls[depth - 1][choice(sub_set)] = 0
                    curr += 1
                    sub_set = [curr]  # Начинаем новый набор
                else:
                    # Удаляем левую стену и добавляем клетку в набор
                    self.app.maze.vertical_walls[depth][curr] = 0
                    curr += 1
                    sub_set.append(curr)
        
        # Удаляем все левые стены в первом ряду
        for i in range(self.app.width - 1):
            self.app.maze.vertical_walls[0][i] = 0
