from calculator_alespool import Calculator
import pytest

def test_add():
    # Test adding two positive integers
    calculator = Calculator()
    result = calculator.add(2, 3)
    assert result == 5

    # Test adding two negative floats
    calculator.reset()
    result = calculator.add(-4.5, -3.5)
    assert result == -8

    # Test adding an integer and a float
    result = calculator.add(5, 2.5)
    assert result == -0.5

    # Test adding an invalid number
    with pytest.raises(ValueError):
        calculator.add('Ale')


def test_subtract():
    # Test subtracting a positive integer from another positive integer
    # Might seem unintuitive, but it's correct as the first number will be subtracted from 0 if we do not add it first
    calculator = Calculator()
    result = calculator.subtract(5, 3)
    assert result == -8

    # Test subtracting a negative float from a negative integer
    result = calculator.subtract(-4, -1.5)
    assert result == -2.5

    # Test subtracting a single number
    calculator.reset()
    result = calculator.subtract(2)
    assert result == -2

def test_multiply():
    # Test multiplying two positive integers
    calculator = Calculator()
    result = calculator.add(2)
    result = calculator.multiply(3)
    assert result == 6

    # Test multiplying a negative float with a positive integer
    calculator.reset()
    result = calculator.add(-4.5)
    result = calculator.multiply(2)
    assert result == -9

    # Test multiplying an invalid number
    with pytest.raises(ValueError):
        calculator.multiply('Ale')


def test_divide():
    # Test dividing a positive integer by another positive integer
    calculator = Calculator()
    calculator.add(10)
    result = calculator.divide(5)
    assert result == 2

    # Test dividing a negative float by a positive integer
    calculator.reset()
    calculator.add(-4.5)
    result = calculator.divide(2)
    assert result == -2.25

    # Test dividing by nothing
    calculator.reset()
    with pytest.raises(TypeError):
        calculator.divide()

    # Test dividing by 0
    with pytest.raises(ZeroDivisionError):
        calculator.divide(0)


def test_root():
    # Test finding the squared root of a positive number
    calculator = Calculator()
    result = calculator.root(9)
    assert result == 3

    # Test finding the cubed root of a negative number
    with pytest.raises(ValueError):
        calculator.root(-8, power=3)

    # Test finding the squared root of a single number
    with pytest.raises(TypeError):
        calculator.root()