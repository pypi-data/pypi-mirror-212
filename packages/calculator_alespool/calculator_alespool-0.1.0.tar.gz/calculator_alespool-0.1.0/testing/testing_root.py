from calculator_alespool import Calculator

calc = Calculator()


def test_root():
    for num in [0.25, -0.25, 2, -2, 8, -8]:
        for power in range(1, 6):
            print('Testing out x = ', str(num), 'and power = ', power)
            result = calc.root(num, power)
            if result is None:
                print('    No root')
            else:
                print('    ', result ** power, '~=', num)


test_root()
