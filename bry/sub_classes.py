class Maze:
    """Класс для представления и управления лабиринтом.

    Attributes:
        app (App): Ссылка на главное приложение для доступа к параметрам.
        horisontal_walls (list[list[int]]): Матрица горизонтальных стен (1 - стена есть, 0 - нет).
        vertical_walls (list[list[int]]): Матрица вертикальных стен (1 - стена есть, 0 - нет).
    """

    def __init__(self, app_):
        """Инициализирует лабиринт с привязкой к главному приложению.
        
        Args:
            app_ (App): Экземпляр главного приложения с параметрами.
        """
        self.app = app_
        self.clear()  # Инициализация стен лабиринта

    def clear(self):
        """Сбрасывает лабиринт в начальное состояние.
        
        В зависимости от выбранного алгоритма создает:
        - Полностью закрытый лабиринт (все стены установлены)
        - Полностью открытый лабиринт (без стен)
        """
        if self.app.algorithm.is_blank:
            # Создаем лабиринт со всеми стенами
            self.horisontal_walls = [[1 for _ in range(self.app.width)] 
                                   for _ in range(self.app.height)]
            self.vertical_walls = [[1 for _ in range(self.app.width - 1)] 
                                 for _ in range(self.app.height)]
        else:
            # Создаем лабиринт без стен
            self.horisontal_walls = [[0 for _ in range(self.app.width)] 
                                   for _ in range(self.app.height)]
            self.vertical_walls = [[0 for _ in range(self.app.width - 1)] 
                                 for _ in range(self.app.height)]
