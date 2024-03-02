class Maze:
    def __init__(self, app_):
        self.app = app_
        self.clear()

    def clear(self):
        if self.app.algorithm.is_blank:
            self.horisontal_walls = [[1 for _1 in range(self.app.width)] for _2 in range(self.app.height)]
            self.vertical_walls = [[1 for _1 in range(self.app.width - 1)] for _2 in range(self.app.height)]
        else:
            self.horisontal_walls = [[0 for _1 in range(self.app.width)] for _2 in range(self.app.height)]
            self.vertical_walls = [[0 for _1 in range(self.app.width - 1)] for _2 in range(self.app.height)]  
