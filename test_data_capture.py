"""
Tests suite for data_capture.
"""
import unittest
from unittest import mock, TestCase

from data_capture import DataCapture, validate_number

class TestDataCapture(TestCase):
    """
    DataCapture tests.
    """
    def test_validate_number(self):
        """
        Tests invalid input types for DataCapture.
        """
        integer_required = ' expected an integer'
        positive_required = ' only accepts a positive'
        with self.assertRaisesRegex(TypeError, 'add' + integer_required):
            validate_number('blah', DataCapture.add)
        with self.assertRaisesRegex(ValueError, 'add' + positive_required):
            validate_number(0, DataCapture.add)

    @mock.patch('data_capture.validate_number')
    def test_add(self, mock_validation):
        """
        Tests that add calls for validation and adds to total_count.
        """
        capture = DataCapture()

        # adding a number should validate it
        capture.add(1)
        mock_validation.assert_called()

        # and increment the total count and individual count
        self.assertEqual(capture.total_count, 1)
        self.assertEqual(capture.numbers[1]['count'], 1)

        # and continue to increment
        capture.add(1)
        self.assertEqual(capture.total_count, 2)
        self.assertEqual(capture.numbers[1]['count'], 2)

        # Adding a different number should increment for that number only
        # and also for the total count.
        capture.add(2)
        self.assertEqual(capture.total_count, 3)
        self.assertEqual(capture.numbers[1]['count'], 2)
        self.assertEqual(capture.numbers[2]['count'], 1)

        with self.assertRaisesRegex(
                ValueError,
                'This method only accepts values up to 999.'
        ):
            capture.add(1000)


class TestStats(TestCase):
    """
    Tests for Stats class.
    """
    @mock.patch('data_capture.validate_number')
    def test_calculations(self, mock_validation):
        """
        Tests calculations for DataCapture.
        """
        capture = DataCapture()
        for number in (3, 9, 3, 4, 6):
            capture.add(number)
        mock_validation.reset_mock()
        stats = capture.build_stats()

        # test with ordinary values
        self.assertEqual(stats.less(4), 2)
        self.assertEqual(stats.between(3, 6), 4)
        # between with number below our lowest count
        self.assertEqual(stats.between(2, 6), 4)
        # between with intermediate number that has no count
        self.assertEqual(stats.between(2, 8), 4)
        # between with number above our highest count
        self.assertEqual(stats.between(4, 10), 3)
        self.assertEqual(stats.greater(4), 2)

        # test with greater than max value
        self.assertEqual(stats.less(1000), 5)
        self.assertEqual(stats.greater(1000), 0)
        self.assertEqual(stats.between(4, 1000), 3)

        # make sure validation was called for each passed number
        self.assertEqual(mock_validation.call_count, 15)


if __name__ == '__main__':
    unittest.main()
