
import unittest

from solvers.ortools_solver import ortools_route


class OrToolsSolverTests(unittest.TestCase):
    def test_route_visits_every_location_once(self):
        matrix = [
            [0.0, 10.0, 15.0, 20.0],
            [10.0, 0.0, 35.0, 25.0],
            [15.0, 35.0, 0.0, 30.0],
            [20.0, 25.0, 30.0, 0.0],
        ]

        route = ortools_route(matrix, start=0)

        self.assertEqual(route[0], 0)
        self.assertEqual(len(route), len(matrix))
        self.assertEqual(set(route), set(range(len(matrix))))

    def test_single_location(self):
        self.assertEqual(ortools_route([[0.0]], start=0), [0])

    def test_rejects_non_square_matrix(self):
        with self.assertRaises(ValueError):
            ortools_route([[0.0, 1.0], [1.0]], start=0)

    def test_rejects_invalid_start(self):
        with self.assertRaises(ValueError):
            ortools_route([[0.0, 1.0], [1.0, 0.0]], start=2)


if __name__ == "__main__":
    unittest.main()
