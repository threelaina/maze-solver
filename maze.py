from components import Window, Cell, Point
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win: Window = None,
        seed=None,
    ):
        if x1 < 0:
            raise ValueError("x1 must be >= 0")
        self.x1 = x1
        if y1 < 0:
            raise ValueError("y1 must be >= 0")
        self.y1 = y1
        if num_rows > 0:
            self.num_rows = num_rows
        else:
            raise ValueError("Number of rows must be > 0")
        if num_cols > 0:
            self.num_cols = num_cols
        else:
            raise ValueError("Number of columns must be > 0")
        if cell_size_x <= 0:
            raise ValueError("cell size must be > 0")
        self.cell_size_x = cell_size_x
        if cell_size_y <= 0:
            raise ValueError("cell size must be > 0")
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            self.seed = random.seed(seed)
        self.seed = seed

        self._create_cells()

    def _create_cells(self):
        self._cells = [[] for x in range(self.num_cols)]
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                top_left = Point(
                    self.x1 + self.cell_size_x * i, self.y1 + self.cell_size_y * j
                )
                bottom_right = Point(
                    top_left.x + self.cell_size_x, top_left.y + self.cell_size_y
                )
                self._cells[i].append(Cell(top_left, bottom_right, self.win))
                self._draw_cell(i, j)

        self._break_entrance_and_exit()

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self.win is not None:
            self.win.redraw()
            time.sleep(0.1)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_right_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _check_neighboring_cell(self, i, j, dir: str):
        current_cell = self._cells[i][j]
        if dir == "left":
            if 0 <= i - 1:
                if (
                    not current_cell.has_left_wall
                    and not self._cells[i - 1][j].has_right_wall
                ):
                    return not self._cells[i - 1][j].visited
        if dir == "right":
            if i + 1 <= self.num_cols - 1:
                if (
                    not current_cell.has_right_wall
                    and not self._cells[i + 1][j].has_left_wall
                ):
                    return not self._cells[i + 1][j].visited
        if dir == "top":
            if 0 <= j - 1:
                if (
                    not current_cell.has_top_wall
                    and not self._cells[i][j - 1].has_bottom_wall
                ):
                    return not self._cells[i][j - 1].visited
        if dir == "bottom":
            if j + 1 <= self.num_rows - 1:
                if (
                    not current_cell.has_bottom_wall
                    and not self._cells[i][j + 1].has_top_wall
                ):
                    return not self._cells[i][j + 1].visited
        return False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        current_cell = self._cells[i][j]
        while True:
            to_visit = []

            if 0 <= i - 1:
                if not self._cells[i - 1][j].visited:
                    to_visit.append((self._cells[i - 1][j], "left"))
            if i + 1 <= self.num_cols - 1:
                if not self._cells[i + 1][j].visited:
                    to_visit.append((self._cells[i + 1][j], "right"))
            if 0 <= j - 1:
                if not self._cells[i][j - 1].visited:
                    to_visit.append((self._cells[i][j - 1], "top"))
            if j + 1 <= self.num_rows - 1:
                if not self._cells[i][j + 1].visited:
                    to_visit.append((self._cells[i][j + 1], "bottom"))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            selected_cell_index = random.randrange(0, len(to_visit))
            to_break = to_visit[selected_cell_index][0]
            dir = to_visit[selected_cell_index][1]

            if dir == "left":  # left cell
                to_break.has_right_wall = False
                current_cell.has_left_wall = False
                self._break_walls_r(i - 1, j)

            if dir == "right":  # right cell
                to_break.has_left_wall = False
                current_cell.has_right_wall = False
                self._break_walls_r(i + 1, j)

            if dir == "top":  # top cell
                to_break.has_bottom_wall = False
                current_cell.has_top_wall = False
                self._break_walls_r(i, j - 1)

            if dir == "bottom":  # bottom cell
                to_break.has_top_wall = False
                current_cell.has_bottom_wall = False
                self._break_walls_r(i, j + 1)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _solve_r(self, i, j):
        current_cell = self._cells[i][j]
        self._animate()
        current_cell.visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        if self._check_neighboring_cell(i, j, "left"):
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            current_cell.draw_move(self._cells[i - 1][j], True)

        if self._check_neighboring_cell(i, j, "right"):
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            current_cell.draw_move(self._cells[i + 1][j], True)

        if self._check_neighboring_cell(i, j, "top"):
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            current_cell.draw_move(self._cells[i][j - 1], True)

        if self._check_neighboring_cell(i, j, "bottom"):
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            current_cell.draw_move(self._cells[i][j + 1], True)

    def solve(self):
        return self._solve_r(0, 0)
