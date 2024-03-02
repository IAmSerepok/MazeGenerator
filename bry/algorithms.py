from random import choice, randint, random
from copy import deepcopy


def check_cell(app, x, y):
        sub_list = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        res = []
        for i, j in sub_list:
            if (i >= 0) and (j >= 0) and (i < app.width) and (j < app.height):
                res.append((i, j))
        return res


class AldousBroder:
    def __init__(self, app):
        self.app = app
        self.is_blank = True
    
    def create_maze(self):
        map = [[0 for _1 in range(self.app.width)] for _2 in range(self.app.height)]
        count = self.app.width * self.app.height - 1
        x, y = randint(0, self.app.width - 1), randint(0, self.app.height - 1)
        map[y][x] = 1
        
        while count:
            sub_list = check_cell(self.app, x, y)
            i, j = choice(sub_list)
            if not map[j][i]:
                count -= 1
                map[j][i] = 1
                self.del_wall(x, y, i, j)
            x, y = i, j
            
    def del_wall(self, x1, y1, x2, y2):
        if x1 == x2:
            self.app.maze.horisontal_walls[min(y1, y2)][x1] = 0
        else:
            self.app.maze.vertical_walls[y1][min(x1, x2)] = 0


class Eller:
    def __init__(self, app):
        self.app = app
        self.is_blank = False
        
    def create_maze(self):
        for _ in range(self.app.height):
            self.create_row(_)

        self.finish_maze()

    def finish_maze(self):
        for i in range(1, self.app.width):
            if self.prev_arr[i-1] != self.prev_arr[i]:
                self.app.maze.vertical_walls[-1][i - 1] = 0

    def create_row(self, depth):
        for i in range(1, self.app.width):
            if (random() <= 0.5) or (self.app.arr[i] == self.app.arr[i - 1]):
                self.app.maze.vertical_walls[depth][i - 1] = 1
            else:
                new_group = self.app.arr[i]
                old_group = self.app.arr[i - 1]
                for _ in range(self.app.width):
                    if self.app.arr[_] == old_group:
                        self.app.arr[_] = new_group

        for i in range(self.app.width):
            if random() <= 0.5:
                self.app.maze.horisontal_walls[depth][i] = 1

        check_arr = [[0, 0, []] for _ in range(self.app.width)]

        for i in range(self.app.width):
            check_arr[self.app.arr[i] - 1][0] += 1
            if self.app.maze.horisontal_walls[depth][i]:
                check_arr[self.app.arr[i] - 1][1] += 1
                check_arr[self.app.arr[i] - 1][2].append(i)

        for count_cell, count_floor, indxes in check_arr:
            if (count_cell == count_floor) and (count_cell != 0):
                tmp = indxes[-1]
                self.app.maze.horisontal_walls[depth][tmp] = 0

        self.prev_arr = deepcopy(self.app.arr)

        for i in range(self.app.width):
            if self.app.maze.horisontal_walls[depth][i]:
                self.app.arr[i] = -1

        nums = [i + 1 for i in range(self.app.width)]

        for i in range(self.app.width):
            if self.app.arr.count(i + 1):
                nums.pop(nums.index(i + 1))

        for i in range(self.app.width):
            if self.app.arr[i] == -1:
                self.app.arr[i] = nums[0]
                nums.pop(0)


class BinaryTree:
    def __init__(self, app):
        self.app = app
        self.is_blank = True
    
    def create_maze(self):
        for depth in range(1, self.app.height):
            for i in range(self.app.width - 1):
                if (random() <= 0.5):
                    self.app.maze.vertical_walls[depth][i] = 0
                else:
                    self.app.maze.horisontal_walls[depth - 1][i] = 0

        for i in range(self.app.width - 1):
            self.app.maze.vertical_walls[0][i] = 0
        for j in range(self.app.height - 1):
            self.app.maze.horisontal_walls[j][-1] = 0


class Sidewinder:
    def __init__(self, app):
        self.app = app
        self.is_blank = True
    
    def create_maze(self):
        for depth in range(1, self.app.height):
            sub_set = [0]
            curr = 0
            
            while curr < self.app.width:
                if (random() <= 0.5) or (curr == self.app.width - 1):
                    self.app.maze.horisontal_walls[depth - 1][choice(sub_set)] = 0
                    curr += 1
                    sub_set = [curr]
                else:
                    self.app.maze.vertical_walls[depth][curr] = 0
                    curr += 1
                    sub_set.append(curr)

        for i in range(self.app.width - 1):
            self.app.maze.vertical_walls[0][i] = 0
