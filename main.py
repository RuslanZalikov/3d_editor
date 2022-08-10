import function

# point_1 = function.Point3d(6, 6, 0)
# point_2 = function.Point3d(6, 11, 0)
# point_3 = function.Point3d(11, 11, -5)
# point_4 = function.Point3d(11, 6, -5)

point_1 = function.Point3d(10, 8, 0)
point_2 = function.Point3d(20, 16, -4)


cube = function.Cube(point_1, point_2)
# line = function.Line3d(point_1, point_2)
# rectangle = function.Rectangle3d(point_1, point_2, point_3, point_4)

matrix = function.Matrix(40, 40)

cube.print(matrix)
# line.print(matrix)
# rectangle.print(matrix)

screen = function.Screen()
screen.updrade(matrix)

# print(line)
# print(rectangle)
# print(cube)

cube.rotation(screen, matrix)
# line.rotation(screen, matrix)
# rectangle.rotation(screen, matrix)

