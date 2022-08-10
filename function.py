import numpy as np
import math
import os


class Point3d:
    def __init__(self, x, y, z=0, angle=math.pi/4):
        self.x3d, self.y3d, self.z3d, self.angle = x, y, z, angle
        self.x = round(self.x3d - self.z3d*math.cos(self.angle))
        self.y = round(self.y3d - self.z3d*math.sin(self.angle))

    def __str__(self):
        return f"\n\tx position {self.x3d}\n\ty position {self.y3d}\n\tz position {self.z3d}" \
               f"\n\tx2d position {self.x}\n\ty2d position {self.y}\n"


class Line3d:
    def __init__(self, pos_first, pos_second):
        self.pos_first, self.pos_second = pos_first, pos_second
        self.len = math.sqrt((self.pos_first.x3d - self.pos_second.x3d)**2+(self.pos_first.y3d - self.pos_second.y3d)**2+(self.pos_first.z3d - self.pos_second.z3d)**2)
        self.len2d = math.sqrt((self.pos_first.x - self.pos_second.x)**2+(self.pos_first.y - self.pos_second.y)**2)
        if self.pos_second.x-self.pos_first.x == 0:
            self.k = 1e9
        elif self.pos_second.y-self.pos_first.y == 0:
            self.k = -1e9
        else:
            self.k = (self.pos_second.y - self.pos_first.y)/(self.pos_second.x-self.pos_first.x)
            self.b = self.pos_first.y - self.k*self.pos_first.x

    def __str__(self):
        return f"First point: {self.pos_first}Second point: {self.pos_second}" \
               f"Length:\n\tlen3d {self.len}\n\tlen2d {self.len2d}"

    def print(self, matrix):
        if self.k == 1e9:
            for index_vector, value_vector in enumerate(matrix.figure):
                if min(self.pos_first.y, self.pos_second.y) <= index_vector <= max(self.pos_first.y, self.pos_second.y) and 0 <= index_vector <= len(matrix.figure) and 0 <= round(self.pos_second.x) <= len(matrix.figure[index_vector]):
                    matrix.figure[index_vector][round(self.pos_second.x)] = "*"
        elif self.k == -1e9:
            for index, value in enumerate(matrix.figure[round(self.pos_first.y)]):
                if min(self.pos_first.x, self.pos_second.x) <= index <= max(self.pos_first.x, self.pos_second.x) and 0 <= round(self.pos_second.y) <= len(matrix.figure) and 0 <= index < len(matrix.figure[round(self.pos_second.y)]):
                    matrix.figure[round(self.pos_second.y)][index] = "*"
        else:
            for index_vector, value_vector in enumerate(matrix.figure):
                for index, value in enumerate(value_vector):
                    if min(self.pos_first.x, self.pos_second.x) <= index <= max(self.pos_first.x, self.pos_second.x) and min(self.pos_first.y, self.pos_second.y) <= index_vector <= max(self.pos_first.y, self.pos_second.y) and 0 <= round(self.k * index + self.b) <= len(matrix.figure) and 0 <= index < len(matrix.figure[round(self.k * index + self.b)]):
                        matrix.figure[round(self.k * index + self.b)][index] = "*"
            for index_vector, value_vector in enumerate(matrix.figure):
                for index, value in enumerate(value_vector):
                    if min(self.pos_first.x, self.pos_second.x) <= index <= max(self.pos_first.x, self.pos_second.x) and min(self.pos_first.y, self.pos_second.y) <= index_vector <= max(self.pos_first.y, self.pos_second.y) and 0 <= index_vector <= len(matrix.figure) and 0 <= round((index_vector - self.b)/self.k) < len(matrix.figure[index_vector]):
                        matrix.figure[index_vector][round((index_vector - self.b)/self.k)] = "*"

    def rotation(self, screen, matrix):
        for angle in range(79, 707):
            self.pos_first = Point3d(self.pos_first.x3d, self.pos_first.y3d, self.pos_first.z3d, angle/100)
            self.pos_second = Point3d(self.pos_second.x3d, self.pos_second.y3d, self.pos_second.z3d, angle/100)
            line = Line3d(self.pos_first, self.pos_second)
            matrix.clear()
            line.print(matrix)
            screen.updrade(matrix)


class Rectangle3d:
    def __init__(self, point_1, point_2, point_3, point_4):
        #point
        self.point_1, self.point_2, self.point_3, self.point_4 = point_1, point_2, point_3, point_4
        #line
        self.left = Line3d(self.point_1, self.point_2)
        self.up = Line3d(self.point_2, self.point_3)
        self.right = Line3d(self.point_3, self.point_4)
        self.down = Line3d(self.point_4, self.point_1)
        #area
        self.area2d = figure_area_2d(self.point_1, self.point_2, self.point_3, self.point_4)

    def __str__(self):
        return f"First point:{self.point_1}" \
               f"Second point:{self.point_2}" \
               f"Three point:{self.point_3}" \
               f"Four point:{self.point_4}" \
               f"Figure area:\n\tarea2d {self.area2d}"

    def print(self, matrix):
        self.left.print(matrix)
        self.up.print(matrix)
        self.right.print(matrix)
        self.down.print(matrix)

    def rotation(self, screen, matrix):
        for angle in range(79, 707):
            self.point_1 = Point3d(self.point_1.x3d, self.point_1.y3d, self.point_1.z3d, angle / 100)
            self.point_2 = Point3d(self.point_2.x3d, self.point_2.y3d, self.point_2.z3d, angle / 100)
            self.point_3 = Point3d(self.point_3.x3d, self.point_3.y3d, self.point_3.z3d, angle / 100)
            self.point_4 = Point3d(self.point_4.x3d, self.point_4.y3d, self.point_4.z3d, angle / 100)
            rectangle = Rectangle3d(self.point_1, self.point_2, self.point_3, self.point_4)
            matrix.clear()
            rectangle.print(matrix)
            screen.updrade(matrix)


class Cube:
    def __init__(self, point_1, point_2):
        #point
        self.point_1 = point_1
        self.point_2 = Point3d(point_1.x3d, point_2.y3d, point_1.z3d, point_1.angle)
        self.point_3 = Point3d(point_2.x3d, point_2.y3d, point_1.z3d, point_1.angle)
        self.point_4 = Point3d(point_2.x3d, point_1.y3d, point_1.z3d, point_1.angle)
        self.point_5 = Point3d(point_1.x3d, point_1.y3d, point_2.z3d, point_1.angle)
        self.point_6 = Point3d(point_1.x3d, point_2.y3d, point_2.z3d, point_1.angle)
        self.point_7 = point_2
        self.point_8 = Point3d(point_2.x3d, point_1.y3d, point_2.z3d, point_1.angle)
        #square
        self.front = Rectangle3d(self.point_1, self.point_2, self.point_3, self.point_4)
        self.back = Rectangle3d(self.point_5, self.point_6, self.point_7, self.point_8)
        self.left = Rectangle3d(self.point_1, self.point_2, self.point_6, self.point_5)
        self.right = Rectangle3d(self.point_4, self.point_3, self.point_7, self.point_8)
        self.up = Rectangle3d(self.point_2, self.point_6, self.point_7, self.point_3)
        self.down = Rectangle3d(self.point_1, self.point_5, self.point_8, self.point_4)
        #area
        self.area3d = abs(self.point_1.x3d - self.point_7.x3d) * abs(self.point_1.y3d - self.point_7.y3d) * abs(self.point_1.z3d - self.point_7.z3d)

    def __str__(self):
        return f"Start point:{self.point_1}" \
               f"Finish point:{self.point_7}" \
               f"Figure area:\n\tarea3d {self.area3d}" \

    def print(self, matrix):
        self.front.print(matrix), self.back.print(matrix)
        self.left.print(matrix), self.right.print(matrix)
        self.up.print(matrix), self.down.print(matrix)

    def rotation(self, screen, matrix):
        for angle in range(79, 707):
            self.point_1 = Point3d(self.point_1.x3d, self.point_1.y3d, self.point_1.z3d, angle / 100)
            self.point_7 = Point3d(self.point_7.x3d, self.point_7.y3d, self.point_7.z3d, angle / 100)
            cube = Cube(self.point_1, self.point_7)
            print(self.point_1.x, self.point_1.y, self.point_7.x, self.point_7.y)
            matrix.clear()
            cube.print(matrix)
            screen.updrade(matrix)


"""в разработке"""
class Rectangle:
    def __init__(self, length, heigth, pos):
        self.lenght, self.heigth, self.pos = length, heigth, pos
        #Point
        self.point_1 = Point3d(self.pos.x, self.pos.y + self.heigth)
        self.point_2 = Point3d(self.pos.x + self.lenght, self.pos.y + self.heigth)
        self.point_3 = Point3d(self.pos.x + self.lenght, self.pos.y)
        #Line
        self.left = Line3d(self.pos, self.point_1)
        self.up = Line3d(self.point_1, self.point_2)
        self.right = Line3d(self.point_2, self.point_3)
        self.down = Line3d(self.point_3, self.pos)

    def print(self, matrix):
        self.left.print(matrix)
        self.up.print(matrix)
        self.right.print(matrix)
        self.down.print(matrix)


class Matrix:
    def __init__(self, length=30, heigth=30):
        self.length, self.heigth = length, heigth
        self.figure = [[" "] * self.length for _ in range(self.heigth)]

    def clone(self, matrix):
        self.figure = matrix.figure

    def clear(self):
        self.figure = [[" "] * self.length for _ in range(self.heigth)]


class Screen:
    def updrade(self, other):
        os.system("clear")
        for value_vactor in reversed(other.figure):
            for value in value_vactor:
                print(value, end=" ")
            print(end="\n")


def figure_area_2d(*point):
    point = list(point)
    first_line = 0
    second_line = 0
    for point_index, point_value in enumerate(point):
        first_line += (point_value.x*point[(point_index+1)%(len(point))].y)
        second_line += (point_value.y*point[(point_index+1)%(len(point))].x)
    return abs(first_line-second_line)/2
