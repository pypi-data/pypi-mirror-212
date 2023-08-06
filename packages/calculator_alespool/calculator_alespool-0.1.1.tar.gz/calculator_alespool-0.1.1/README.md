# Calculator

This is a Python project developing a calculator that can perform basic arithmetic operations of addition, subtraction,
 multiplication and division. It can also take the (n) root of a number. The calculator has an internal memory with 
default value of 0.


## Getting Started

### Requirements

This project requires Python 3.6 or greater with the typing package which is used for type annotations. For testing 
the scripts, pytest and unittest packages are used.


## Installation

You can install this project using pip:

`$ pip install calculator_alespool`

## Usage

The Calculator class can be used to perform simple arithmetic operations. To use the Calculator, first create an instance of it:

```
from calculator_alespool import Calculator`
calculator = Calculator()
```

You can then use the add(), subtract(), multiply(), divide() and root() methods of the Calculator object to perform operations.

IMPORTANT: Remember that this calculator starts with a default value of 0. When operations are made, the result
is stored in its memory and thus changing operation without calling a reset of the memory will result in wrong and/or unwanted results.

IMPORTANT: Except for the add() method, all the other methods follow the concept that without a value they don't know what to do. 
Whether there is a value in the memory or not, it is not possible to just select 2 numbers and expect the result to be 
declared using those 2 numbers. Calling multiplication(2,3) will not result in 6, but 0 because it multiplies by the 
internal value of the memory which is set at 0 when the calculator has no value in its memory.

#### Addition

For example, to add two numbers:

```
result = calculator.add(2, 3)
print(result)
# Output: 5
```
The numbers are not just summed together. First, the 2 is added to the internal memory, then the 3 is added.

#### Subtraction

To subtract numbers, since the default memory value is of 0, it is not possible to simply select two numbers to subtract
from. It is necessary to add the initial number first, and then select the subtraction function to subtract a selected
number from the initial one.

To subtract two numbers:
```
calculator.reset() # renders internal memory to 0
result = calculator.add(5) 
result = calculator.subtract(3)
print(result)
# Output: 2
```

The number is first added into the internal memory, and then a second number is subtracted from it.

### Multiplication

For the multiplication, the wanted results can be obtained as follows:

```
result = calculator.add(2)
result = calculator.multiply(3)
# Output 6
```

### Division

The divide() method does some more checks than previous methods. This is because it raises a ZeroDivisionError when the 
outcome seems to be a division by 0.

```
calculator.reset()
calculator.add(3)
calculator.divide()
# Output: You can't divide by 0
Traceback (most recent call last):
  File "~/calculator_alespool.py", line 309, in <module>
    result = calculator.divide(0)
             ^^^^^^^^^^^^^^^^^^^^
  File "~/calculator_alespool.py", line 207, in divide
    raise ZeroDivisionError
ZeroDivisionError

Process finished with exit code 1

```

When asked to divide by nothing, or nothing is entered in the arguments position, it returns a TypeError.

```
calculator.reset()
calculator.divide()

# Output: Traceback (most recent call last):
  File "~/calculator_alespool.py", line 309, in <module>
    result = calculator.divide()
             ^^^^^^^^^^^^^^^^^^^
TypeError: Calculator.divide() missing 1 required positional argument: 'num'
```

### (n) root of number

To take the (n) root of a number, it is important that this number is not negative. The default value of the (n)
root is 2, meaning if not specified a square root value is returned. When asked to take (n) root of a negative number, 
a ValueError message is raised:

```
calculator.root(-2)
# Output: Cannot compute square root of a negative number. Try again...
Traceback (most recent call last):
  File "~/calculator_alespool.py", line 313, in <module>
    result = calculator.root(-2)
             ^^^^^^^^^^^^^^^^^^^
  File "~/calculator_alespool.py", line 271, in root
    raise ValueError
ValueError
```

A peculiarity of this method is that when the result is a whole number, it is turned into an integer. The conditional 
statement governing this change checks whether the remainder of the division between the value currently set in the 
internal memory and 1 is equal to 0. If so, it means that this value is an integer.

```
if current_value % 1 == 0:
    return int(current_value)
```

To obtain square root value, this is the procedure: 
```
calculator.add(9)
result = calculator.root()
# Output: 3
```

You can also specify a custom power for the root operation using the power parameter:
```
calculator.add(27)
result = calculator.root(power=3)
# Output: 3
```

## Other methods functions

You can also pass an iterable of numbers to all of these mathematical operations method with `*args`:\

```
numbers = [2, 3, 4, 5]

result = calculator.add(*numbers)
calculator.reset()

result = calculator.subtract(*numbers)
calculator.reset()

result = calculator.multiply(*numbers)
calculator.reset()

result = calculator.divide(*numbers)
calculator.reset()

result = calculator.root(*numbers)
calculator.reset()

Add output: 14
Subtract output: -14
Multiply output: 0
Divide output: 0
Root output: 2.23606797749979
```

This may come in handy in case you know which are the next numbers you want to further work with.

## Running Tests

This project includes a testing module that can be run using the pytest framework.

To run the tests, first install pytest and unittest:

`$ pip install pytest`

`$ pip install unittest`

You can then run the tests using the pytest and unittest command:

`$ pytest`

`$ unittest`

# License

This project is licensed under the MIT License. See the LICENSE file for more information.