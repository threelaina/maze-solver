from components import Window
from maze import Maze


def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 10, 10, 30, 30, win)
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    maze.solve()
    win.wait_for_close()


main()
