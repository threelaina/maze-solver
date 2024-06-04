import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells2(self):
        num_cols = 15
        num_rows = 9
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_zero_columns(self):
        num_cols = 0
        num_rows = 10
        with self.assertRaises(Exception):
            Maze(0, 0, num_rows, num_cols, 10, 10)

    def test_maze_zero_rows(self):
        num_cols = 5
        num_rows = 0
        with self.assertRaises(Exception):
            Maze(0, 0, num_rows, num_cols, 10, 10)

    def test_maze_neg_rows(self):
        num_cols = 5
        num_rows = -7
        with self.assertRaises(Exception):
            Maze(0, 0, num_rows, num_cols, 10, 10)

    def test_maze_neg_cols(self):
        num_cols = -2
        num_rows = 5
        with self.assertRaises(Exception):
            Maze(0, 0, num_rows, num_cols, 10, 10)

    def test_maze_invalid_x1(self):
        x1 = -1
        y1 = 0
        with self.assertRaises(Exception):
            Maze(x1, y1, 5, 5, 10, 10)

    def test_maze_invalid_y1(self):
        x1 = 0
        y1 = -5
        with self.assertRaises(Exception):
            Maze(x1, y1, 5, 5, 10, 10)

    def test_maze_invalid_cell_size_x(self):
        cell_size_x = 0
        cell_size_y = 10
        with self.assertRaises(Exception):
            Maze(10, 10, 5, 5, cell_size_x, cell_size_y)

    def test_maze_invalid_cell_size_y(self):
        cell_size_x = 10
        cell_size_y = 0
        with self.assertRaises(Exception):
            Maze(10, 10, 5, 5, cell_size_x, cell_size_y)

    def test_break_walls(self):
        pass

    def test_rest_cells_visited(self):
        pass


if __name__ == "__main__":
    unittest.main()
