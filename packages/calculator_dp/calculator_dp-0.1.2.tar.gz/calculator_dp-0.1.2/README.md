# Basic Calculator

> Python class for basic math operations.

Package `mycalculator` contains Python class `Calculator` that performs basic mathematical operations:

- addition;
- subtraction;
- multiplication;
- division;
- taking n-th root.


## Details

Class attributes:

- `.result` -- read-only attribute, returns a numeric value of current result `.__result`.
   Initial (default) value of `.__result` is 0.

Class methods:

- `.add(value)` -- This method performs addition of numeric value of `.__result` (class attribute) and `value` (parameter) and saves the result as `.__result`.
- `.subtract(value)` -- This method performs subtraction of numeric value of `.__result` (class attribute) and `value` (parameter) and saves the result as `.__result`.
- `.multiply_by(value)` -- This method performs multiplication of numeric value of `.__result` (class attribute) and `value` (parameter) and saves the result as `.__result`.
- `.divide_by(value)` -- This method performs division of numeric value of `.__result` (class attribute) and `value` (parameter) and saves the result as `.__result`.
- `.root_by(value)` -- This method performs taking n-th root of numeric value of `.__result` (class attribute) and `value` (parameter) and saves the result as `.__result`.
- `.reset()` -- This method resets the `.__result` to 0 (default).   

## Installation

```sh
pip install calculator_dp
```

## Examples

```python
>>> from mycalculator.calculator import Calculator

>>> calculator = Calculator()
>>> calculator.add(5)
>>> calculator.result
5.0
>>> calculator.reset()
>>> calculator.result
0.0
>>> calculator.subtract(5)
>>> calculator.result
-5.0
>>> calculator.add(105)
>>> calculator.root_by(2)
>>> calculator.result
10.0
>>> calculator.reset()
>>> calculator.result
0.0
```

## License

[MIT](https://choosealicense.com/licenses/mit/)