'Creating a calculator that can be used to add, subtract, multiply, divide and take (n) root power'

__version__ = "0.1.1"

from typing import Union, Iterable, Optional


class Calculator:
    """An attempt to create a calculator."""

    def __init__(self):
        self.current_value = 0

    def __repr__(self):
        return f"The current value is {self.current_value}"

    def add(self, num: Union[int, float], *args: Union[int, float]) -> Union[int, float]:
        """
        Takes in a series of numbers as iterable and sums them up.

        If the iterable is empty, or has only one value, the function is invalid.

        :param num: Any number `int` or `float` to be added.
        :param args: Creates an iterable of any number. Can be `int` or `float`.
        :return: Return the sum of the 'start' value (default: 0) plus an iterable of numbers.

        Examples:
        ------------------------
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
        """

        if not isinstance(num, (int, float)):
            print("Insert only valid numbers (integers or floats).  Try again...")
            raise ValueError

        self.current_value += num

        # If there are additional arguments, continue processing them
        if args:
            for additional_num in args:
                if isinstance(additional_num, (int, float)):
                    self.current_value += additional_num
                else:
                    print("Insert only valid numbers (integers or floats).  Try again...")
                    self.current_value = 0
                    raise ValueError

        return self.current_value

    def subtract(self, num: Union[int, float], *args: Iterable[Union[int, float]]) -> Union[int, float]:
        """
        Takes in a series of numbers as iterable and subtracts them to the starting value of the first number.

        If the iterable is empty, the function returns 0.

        :param num: Any number `int` or `float` to be subtracted
        :param args: Creates an iterable of any number. Can be `int` or `float`.
        :return: Return the subtraction of the default values (start: 0) and an iterable of other numbers.

        Examples:
        ------------------------
        # Test subtracting a positive integer from another positive integer
        # Might seem unintuitive, but it's correct to have a negative result as
        the first number will be subtracted from 0 if we don't add it first
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
        """

        if not isinstance(num, (int, float)):
            print("Insert only valid numbers (integers or floats).  Try again...")
            raise ValueError

        self.current_value -= num

        # If there are additional arguments, continue processing them
        if args:
            for additional_num in args:
                if isinstance(additional_num, (int, float)):
                    self.current_value -= additional_num
                else:
                    print("Insert only valid numbers (integers or floats).  Try again...")
                    self.current_value = 0
                    raise ValueError

        return self.current_value

    def multiply(self, num: Union[float, int], *args: Iterable[Union[int, float]]) -> Union[int, float]:
        """
        Takes in an iterable and returns the result of the multiplication of each number by the previous one.

        If the iterable is empty, it returns 0. If only one number is entered,
        it acts as a multiplication by 0 and returns 1.

        :param num: Any number `int` or `float` to be multiplied.
        :param args: Creates an iterable of any number. Can be `int` or `float`
        :return: Returns the multiplication of numbers in an iterable.


        Examples:
        ------------------------
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
        """

        if not isinstance(num, (int, float)):
            print("Insert only valid numbers (integers or floats).  Try again...")
            raise ValueError

        self.current_value *= num

        # If there are additional arguments, continue processing them
        if args:
            for additional_num in args:
                if isinstance(additional_num, (int, float)):
                    self.current_value *= additional_num
                else:
                    print("Insert only valid numbers (integers or floats).  Try again...")
                    self.current_value = 0
                    raise ValueError

        return self.current_value

    def divide(self, num: Union[float, int], *args: Iterable[Union[int, float]]) -> Union[int, float]:
        """
        Takes in a series of numbers as iterable and divides them from the starting value of the first number.

        If the iterable is empty, the function returns 0. It handles division by 0 by raising exception.

        :param num: Any number `int` or `float` to be divided.
        :param args: Creates an iterable of any number. Can be `int` or `float`.
        :return: Return the division of the values inputted as iterables.

        Examples:
        ------------------------
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
        """

        if not isinstance(num, (int, float)):
            print("Insert only valid numbers (integers or floats).  Try again...")
            raise ValueError

        if num is None:
            print("You can't divide by nothing.")
            raise TypeError
        elif num == 0:
            print("You can't divide by 0")
            raise ZeroDivisionError

        self.current_value /= num

        # If there are additional arguments, continue processing them
        if args:
            for additional_num in args:
                if isinstance(additional_num, (int, float)):
                    try:
                        self.current_value /= additional_num
                    except ZeroDivisionError:
                        print("You can't divide by zero.")
                        pass
                else:
                    print("Insert only valid numbers (integers or floats).  Try again...")
                    self.current_value = 0
                    raise ValueError

        if self.current_value % 1 == 0:
            return int(self.current_value)
        else:
            return self.current_value

    def root(self, num: Optional[Union[float, int]] = None, power: int = 2, *args: Iterable[Union[int, float]] ) -> \
            Union[int, float]:
        """
        Returns the closest approximation of the root of the chosen power for the inputted number.
        The default value of the power is 2.

        :param power: An `int`. Determines the power of the root operation. Default value: 2 (squared root)
        :param num: Can be `int` or `float`.
        :return: A float value, representing the square power of a number within the epsilon of x

        Examples:
        ------------------------
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
        """

        # Check for negative power
        if power == 0:
            raise ValueError("Cannot compute root of zero power.")
        if power < 0:
            raise ValueError("Cannot compute negative power root.")

        # Not able to write code for negative numbers roots
        if num is None:
            if self.current_value < 0:
                raise ValueError("Cannot compute square root of a negative number. "
                                 "Please use a calculator that handles complex numbers.")

            elif self.current_value == 0:
                print("You can't get a root of no number.")
                raise TypeError

            else:
                self.current_value = self.current_value ** (1 / power)

        elif num < 0:
            print("Cannot compute square root of a negative number. Try again...")
            self.current_value = 0
            raise ValueError
        else:
            self.current_value = num ** (1 / power)

        # If there are additional arguments, continue processing them
        if args:
            for additional_num in args:
                if isinstance(additional_num, (int, float)):
                    self.current_value = additional_num ** (1 / power)
                else:
                    print("Insert only valid numbers (integers or floats). Try again...")
                    self.current_value = 0
                    raise ValueError

        if self.current_value % 1 == 0:
            return int(self.current_value)

        return self.current_value

    def reset(self):
        self.current_value = 0
        print("The memory of the calculator has been erased.")
        return self.current_value
