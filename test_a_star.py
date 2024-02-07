import unittest
from astar import a_star  

class TestAStar(unittest.TestCase):

    def test_case_1(self):
        inf_pitcher = 100000
        capacities = (inf_pitcher, 1, 4, 10, 15, 22)
        target_quantity = 181
        expected_steps = 20
        self.assertEqual(a_star(capacities, target_quantity), expected_steps)

    def test_case_2(self):
        inf_pitcher = 100000
        capacities = (inf_pitcher, 2, 5, 6, 72)
        target_quantity = 143
        expected_steps = 7
        self.assertEqual(a_star(capacities, target_quantity), expected_steps)

    def test_case_3(self):
        inf_pitcher = 100000
        capacities = (inf_pitcher, 3, 6)
        target_quantity = 2
        expected_steps = -1
        self.assertEqual(a_star(capacities, target_quantity), expected_steps)

    def test_case_4(self):
        inf_pitcher = 100000
        capacities = (inf_pitcher, 2)
        target_quantity = 143
        expected_steps = -1
        self.assertEqual(a_star(capacities, target_quantity), expected_steps)

    def test_case_5(self):
        inf_pitcher = 100000
        capacities = (inf_pitcher, 2, 3, 5, 19, 121, 852)
        target = 11443
        expected = 36
        self.assertEqual(a_star(capacities, target), expected)

if __name__ == '__main__':
    unittest.main()
