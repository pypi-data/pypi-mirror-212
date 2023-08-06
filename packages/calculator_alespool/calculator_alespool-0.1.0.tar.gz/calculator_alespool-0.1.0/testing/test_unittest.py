import unittest
from calculator_alespool import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_addition(self):
        self.assertEqual(self.calc.add(1, 2, 4), 7)
        self.assertEqual(self.calc.add(1, 2, 4), 14)
        self.calc.reset()
        self.assertEqual(self.calc.add(1, 2, 4), 7)

    def test_subtraction(self):
        self.assertEqual(self.calc.subtract(1), -1)
        self.assertEqual(self.calc.subtract(1, 2, 3), -7)
        self.calc.reset()
        self.assertEqual(self.calc.add(1, 2, 4), 7)
        self.assertEqual(self.calc.subtract(1, 3, 4), -1)
        self.assertEqual(self.calc.subtract(1.2), -2.2)

    def test_multiplication(self):
        self.assertEqual(self.calc.multiply(1), 0)
        self.assertEqual(self.calc.multiply(1, 2, 3), 0)
        self.assertEqual(self.calc.multiply(-2), 0)
        self.calc.reset()
        self.assertEqual(self.calc.add(1, 2, 4), 7)
        self.assertEqual(self.calc.subtract(1, 3, 4), -1)
        self.assertEqual(self.calc.multiply(3), -3)

    def test_division(self):
        self.assertEqual(self.calc.current_value, 0)
        self.assertEqual(self.calc.add(3), 3)
        self.assertEqual(self.calc.add(50), 53)
        self.assertEqual(self.calc.divide(5), 10.6)
        self.assertEqual(self.calc.divide(2, 2), 2.65)
        self.assertEqual(self.calc.divide(2.5), 1.06)
        self.assertRaises(ZeroDivisionError, self.calc.divide, 0)
        self.calc.reset()
        self.assertEqual(self.calc.add(25), 25)
        self.assertEqual(self.calc.divide(5), 5)

    def test_root(self):
        self.assertEqual(self.calc.current_value, 0)
        self.calc.reset()
        self.assertEqual(self.calc.add(16), 16)
        self.assertEqual(self.calc.root(4), 2)
        self.calc.reset()
        self.assertEqual(self.calc.add(16), 16)
        self.assertEqual(self.calc.root(), 4)
        self.calc.reset()
        self.assertEqual(self.calc.subtract(10), -10)
        self.assertEqual(0, self.calc.root())

    def test_chained_operations(self):
        self.calc.add(5)
        self.assertEqual(self.calc.add(3), 8)
        self.assertEqual(self.calc.root(), 2.8284271247461903)


if __name__ == '__main__':
    unittest.main()