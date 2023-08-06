"""main.py is used to check the functionality of mycalculator.calculator
module.
"""


if __name__ == "__main__":
    from mycalculator.calculator import Calculator

    calculator = Calculator()
    print(f"Initializing. Default result: {calculator.result}")

    calculator.add(100)
    print(f"Calling: add 100. Result: {calculator.result}")

    calculator.subtract(50)
    print(f"Calling: subtract 50. Result: {calculator.result}")

    calculator.multiple_by(4)
    print(f"Calling: multiple_by 4. Result: {calculator.result}")

    calculator.divide_by(2)
    print(f"Calling: divide_by 2. Result: {calculator.result}")

    calculator.root_by(2)
    print(f"Calling: root_by 2. Result: {calculator.result}")

    calculator.reset()
    print(f"Calling: reset. Result: {calculator.result}")

    # calculator.__result += 12   # returns AttributeError
