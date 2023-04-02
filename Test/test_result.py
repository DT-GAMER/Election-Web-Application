import unittest
from result import get_results

class TestResult(unittest.TestCase):
    def test_get_results(self):
        expected = [
            {'name': 'Alli_Kamal Mazeedah', 'position': 'Sport Secretary', 'votes': 50},
            {'name': 'Ayo Babalola Samuel', 'position': 'Sport Secretary', 'votes': 35},
            {'name': 'Farinloye Susan Folake', 'position': 'Sport Secretary', 'votes': 15}
        ]
        actual = get_results()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

