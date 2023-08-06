"""This module contains class `Calculator` which performs simple math
operations."""


class Calculator:
    """Class to do following math operations:

    * addition / subtraction
    * Multiplication / Division
    * Take (n) root of a number

    Calculator performs specified math operations with the value of attribute
    `result` (initial value is 0). This attribute is read-only outside the
    class.

    To reset attribute `result` value to 0, call `reset` method.

    Examples
    ---------
    >>> calculator = Calculator()
    >>> print(calculator.result)
    0.0
    >>> calculator.add(5)
    >>> print(calculator.result)
    5.0
    >>> calculator.multiple_by(3)
    >>> print(calculator.result)
    15.0
    >>> calculator.reset()
    >>> print(calculator.result)
    0.0
    """

    @property
    # Property decorator - read-only attribute
    def result(self) -> float:
        """Initializing class object"""
        return self.__result

    def __init__(self) -> None:
        self.__result = 0.0

    def add(self, value: float) -> None:
        """Add `value` to a value of attribute `result` and save
        result to `result`

        Args
        ---------
        value (float): The value that will be added to `result`

        Returns
        ---------
        None. Updates the value of attribute `result` with a result
        of performed mathematical operation.

        Examples
        ---------
        >>> calculator = Calculator()
        >>> calculator.add(5)
        >>> print(calculator.result)
        5.0
        """
        self.__result += value

    def subtract(self, value: float) -> None:
        """Subtract `value` from a value of attribute `result` and save
        result to `result`

        Args
        ---------
        value (float): The value that will be subtracted from `result`

        Returns
        ---------
        None. Updates the value of attribute `result` with a result
        of performed mathematical operation.

        Examples
        ---------
        >>> calculator = Calculator()
        >>> calculator.subtract(2)
        >>> print(calculator.result)
        -2.0
        """
        self.__result -= value

    def multiple_by(self, value: float) -> None:
        """Multiply a value of attribute `result` by a `value` and save
        result to `result`

        Args
        ---------
        value (float): The value that `result` will be multiplied by.

        Returns
        ---------
        None. Updates the value of attribute `result` with a result
        of performed mathematical operation.

        Examples
        ---------
        >>> calculator = Calculator()
        >>> calculator.add(10)
        >>> calculator.multiple_by(2)
        >>> print(calculator.result)
        20.0
        """
        self.__result = self.__result * value

    def divide_by(self, value: float) -> None:
        """Divide a value of attribute `result` by a `value` and save
        result to `result`

        Args
        ---------
        value (float): The value that `result` will be divided by.

        Returns
        ---------
        None. Updates the value of attribute `result` with a result
        of performed mathematical operation.

        Examples
        ---------
        >>> calculator = Calculator()
        >>> calculator.add(10)
        >>> calculator.divide_by(2)
        >>> print(calculator.result)
        5.0
        """
        self.__result = self.__result / value

    def root_by(self, value: float) -> None:
        """Take `value` root of the value of attribute `result` and save
        result to `result`

        Args
        ---------
        value (float): Degree of root.

        Returns
        ---------
        None. Updates the value of attribute `result` with a result
        of performed mathematical operation.

        Examples
        ---------
        >>> calculator = Calculator()
        >>> calculator.add(100)
        >>> calculator.root_by(2)
        >>> print(calculator.result)
        10.0
        """
        self.__result = self.__result ** (1 / value)

    def reset(self) -> None:
        """Reset the value of attribute `result`.

        Returns
        ---------
        None. Resets the value of attribute `result` to 0.

        Examples
        ---------
        >>> calculator = Calculator()
        >>> calculator.add(100)
        >>> calculator.reset()
        >>> print(calculator.result)
        0.0
        """
        self.__result = 0.0


# if __name__ == "__main__":
#    import doctest
#
#    print(doctest.testmod())
