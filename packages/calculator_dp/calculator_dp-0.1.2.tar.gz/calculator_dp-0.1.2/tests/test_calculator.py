import pytest
from mycalculator.calculator import Calculator


def test_init():
    calculator = Calculator()
    assert calculator.result == 0


def test_add():
    calculator = Calculator()
    calculator.add(5)
    assert calculator.result == 5


def test_add_wrong_inputs():
    calculator = Calculator()
    # Input is str instead of float:
    with pytest.raises(TypeError):
        calculator.add("5")
    # Input is list instead of float:
    with pytest.raises(TypeError):
        calculator.add([5])
    # Too many args:
    with pytest.raises(TypeError):
        calculator.add(5, 5)


def test_subtract():
    calculator = Calculator()
    calculator.subtract(5)
    assert calculator.result == -5


def test_subtract_wrong_inputs():
    calculator = Calculator()
    # Input is str instead of float:
    with pytest.raises(TypeError):
        calculator.add("5")
    # Input is list instead of float:
    with pytest.raises(TypeError):
        calculator.add([5])
    # Too many args:
    with pytest.raises(TypeError):
        calculator.add(5, 5)


def test_multiple_by():
    calculator = Calculator()
    calculator.add(5)
    calculator.multiple_by(5)
    assert calculator.result == 25
    calculator.multiple_by(-2)
    assert calculator.result == -50
    calculator.multiple_by(0)
    assert calculator.result == 0


def test_multiple_by_wrong_inputs():
    calculator = Calculator()
    # Input is str instead of float:
    with pytest.raises(TypeError):
        calculator.multiple_by("5")
    # Input is list instead of float:
    with pytest.raises(TypeError):
        calculator.multiple_by([5])
    # Too many args:
    with pytest.raises(TypeError):
        calculator.multiple_by(5, 5)


def test_divide_by():
    calculator = Calculator()
    calculator.add(20)
    calculator.divide_by(2)
    assert calculator.result == 10
    calculator.divide_by(-2)
    assert calculator.result == -5


def test_divide_by_wrong_inputs():
    calculator = Calculator()
    calculator.add(20)
    # Input is str instead of float:
    with pytest.raises(TypeError):
        calculator.divide_by("5")
    # Input is list instead of float:
    with pytest.raises(TypeError):
        calculator.divide_by([5])
    # Too many args:
    with pytest.raises(TypeError):
        calculator.divide_by(5, 5)


def test_divide_by_zero():
    calculator = Calculator()
    calculator.add(20)
    with pytest.raises(ZeroDivisionError):
        calculator.divide_by(0)


def test_root_by():
    calculator = Calculator()
    calculator.add(100)
    calculator.root_by(2)
    assert calculator.result == 10
    calculator.add(90)
    calculator.root_by(-2)
    assert calculator.result == 0.1


def test_root_by_wrong_inputs():
    calculator = Calculator()
    calculator.add(100)
    # Input is str instead of float:
    with pytest.raises(TypeError):
        calculator.root_by("5")
    # Input is list instead of float:
    with pytest.raises(TypeError):
        calculator.root_by([5])
    # Too many args:
    with pytest.raises(TypeError):
        calculator.root_by(5, 5)


def test_root_by_zero():
    calculator = Calculator()
    calculator.add(20)
    with pytest.raises(ZeroDivisionError):
        calculator.root_by(0)


def test_reset():
    calculator = Calculator()
    calculator.add(5)
    calculator.reset()
    assert calculator.result == 0
