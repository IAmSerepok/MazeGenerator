from browser import document
from sub_classes import *
from algorithms import *


class App:
    def __init__(self):

        self.brython_init()
        self.size_init(1, 1)
        
        self.arr = [i + 1 for i in range(self.width)]
        self.prev_arr = []
        
        self.algorithms = [AldousBroder(self), BinaryTree(self), Sidewinder(self)]
        self.algorithm_indx = 0
        self.algorithm = self.algorithms[self.algorithm_indx]
        self.maze = Maze(self)

    def size_init(self, width, height):
        self.width = width
        self.height = height
        
        self.cell_size = (self.canvas.width / self.width, self.canvas.height / self.height)

        
    def brython_init(self):
        self.canvas = document['myCanvas']
        self.width_inp = document['myWidth']
        self.height_inp = document['myHeight']
        self.algorithm_inp = document['myAlgorithm']

        self.ctx = self.canvas.getContext("2d")

        document["myButton"].bind("click", self.generate)
        
    def generate(self, ev):
        if self.width_inp.value and self.height_inp.value:
            self.size_init(int(self.width_inp.value), int(self.height_inp.value))

        self.algorithm_indx = int(self.algorithm_inp.value)
        self.algorithm = self.algorithms[self.algorithm_indx]
        self.maze.clear()
        self.algorithm.create_maze()
        self.draw()

    def draw(self):
        ctx = self.ctx

        ctx.beginPath()
        ctx.rect(0, 0, self.canvas.width, self.canvas.height, 1)
        ctx.fillStyle = "#0a0a0a"
        ctx.fill()
        ctx.closePath()

        for i in range(self.height - 1):
            for j in range(self.width):
                if self.maze.horisontal_walls[i][j]:
                    ctx.beginPath()
                    ctx.rect(j * self.cell_size[0], (i + 1) * self.cell_size[1], self.cell_size[0], 1)
                    ctx.fillStyle = "#FFFFFF"
                    ctx.fill()
                    ctx.closePath()

        for i in range(self.height):
            for j in range(self.width - 1):
                if self.maze.vertical_walls[i][j]:
                    ctx.beginPath()
                    ctx.rect((j + 1) * self.cell_size[0], i * self.cell_size[1], 1, self.cell_size[1])
                    ctx.fillStyle = "#FFFFFF"
                    ctx.fill()
                    ctx.closePath()


app = App()
