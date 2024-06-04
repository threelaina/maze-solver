from tkinter import Tk, Canvas


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        x1 = self.point1.x
        y1 = self.point1.y
        x2 = self.point2.x
        y2 = self.point2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(height=self.height, width=self.width)
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, top_left: Point, bottom_right: Point, win: Window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = top_left.x
        self._x2 = bottom_right.x
        self._y1 = top_left.y
        self._y2 = bottom_right.y
        self._center = Point((self._x2 + self._x1) / 2, (self._y2 + self._y1) / 2)
        self.win = win
        self.visited = False

    def draw(self):
        default_color = "black"
        invisible_color = "#d9d9d9"

        if self.win is None:
            raise Exception("window must be provided to draw walls")

        left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        if self.has_left_wall:
            left_wall.draw(self.win.canvas, default_color)
        else:
            left_wall.draw(self.win.canvas, invisible_color)

        right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        if self.has_right_wall:
            right_wall.draw(self.win.canvas, default_color)
        else:
            right_wall.draw(self.win.canvas, invisible_color)

        top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        if self.has_top_wall:
            top_wall.draw(self.win.canvas, default_color)
        else:
            top_wall.draw(self.win.canvas, invisible_color)

        bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        if self.has_bottom_wall:
            bottom_wall.draw(self.win.canvas, default_color)
        else:
            bottom_wall.draw(self.win.canvas, invisible_color)

    def draw_move(self, to_cell, undo=False):
        connecting_line = Line(self._center, to_cell._center)
        if undo:
            line_color = "gray"
        else:
            line_color = "red"
        connecting_line.draw(self.win.canvas, line_color)
