"""DataCapture module."""
from collections import OrderedDict

COUNT = 'count'
GREATER_THAN = 'greater_than'
LESS_THAN = 'less_than'

MAX_VAL = 999


def validate_number(number, func, many=False):
    """
    Ensure that the number is a positive int.
    """
    # I think this has the potential to be switched to a decorator,
    # so prefer passing in the function instead of its name
    # to make changing this easier later.
    function_name = func.__name__

    if not isinstance(number, int) or isinstance(number, bool):
        int_string = 'integers' if many else 'an integer'
        error_message = f'{function_name} expected {int_string}.'
        raise TypeError(error_message)
    if number < 1:
        int_string = 'positive integers' if many else 'a positive integer'
        error_message = f'{function_name} only accepts {int_string}.'
        raise ValueError(error_message)


class DataCapture:
    """
    Captures numerical data for analysis.
    """
    def __init__(self):
        self.numbers = OrderedDict(
            **{num: {COUNT: 0} for num in range(MAX_VAL)}
        )
        self.total_count = 0

    def add(self, number):
        """
        Adds an integer to the captured data.

        Only accepts values under MAX_VAL.
        """
        validate_number(number, self.add)
        if number > MAX_VAL:
            error_message = f'This method only accepts values up to {MAX_VAL}.'
            raise ValueError(error_message)
        self.numbers[number][COUNT] += 1
        self.total_count += 1

    def build_stats(self):
        """
        Returns a Stats instance generated from the captured data.

        Note:
            This could probably be more efficient.
            The current approach will always iterate over MAX_VAL values.
            I could have used a try-except when accessing the numbers
            to check for higher or lower keys in the Stats calculations,
            but without some optimization
            that would add more time to those calculations.
            It seemed like adding to the stats building time
            would be more tolerable for the user.
        """
        lesser_count = 0
        greater_count = self.total_count
        for number in self.numbers:
            number_count = self.numbers[number][COUNT]
            self.numbers[number][LESS_THAN] = lesser_count
            self.numbers[number][GREATER_THAN] = greater_count - number_count
            lesser_count += number_count
            greater_count -= number_count

        return Stats(numbers=self.numbers, total_count=self.total_count)


class Stats:
    """
    Stats calculated by DataCapture.
    """
    def __init__(self, numbers, total_count):
        self.numbers = numbers
        self.total_count = total_count

    def less(self, number):
        """
        Returns the count of all numbers below the submitted number.
        """
        validate_number(number, self.less)
        if number > MAX_VAL:
            return self.total_count
        return self.numbers[number][LESS_THAN]

    def greater(self, number):
        """
        Returns the count of all numbers above the submitted number.
        """
        validate_number(number, self.greater)
        if number > MAX_VAL:
            return 0
        return self.numbers[number][GREATER_THAN]

    def between(self, first_number, second_number):
        """
        Returns the count of all numbers
        between first_number and second_number, inclusive.
        """
        for number in (first_number, second_number):
            validate_number(
                number,
                self.between,
                many=True
            )
        low_number, high_number = (
            (first_number, second_number)
            if first_number < second_number
            else (second_number, first_number)
        )
        numbers = self.numbers
        if high_number > MAX_VAL:
            return self.total_count - self.less(low_number)
        high_num_dict = numbers[high_number]
        less_than_high_num = high_num_dict[LESS_THAN] + high_num_dict[COUNT]
        less_than_low_num = numbers[low_number][LESS_THAN]
        return less_than_high_num - less_than_low_num
