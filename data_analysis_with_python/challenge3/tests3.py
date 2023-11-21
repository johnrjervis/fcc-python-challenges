import unittest as ut
from solution3 import binary_limit

class BinaryLimitTests(ut.TestCase):
    """Tests for the binary_limit function"""

    def test_binary_limit_returns_zero_for_an_input_of_one_if_no_threshold_supplied(self):
        self.assertEqual(binary_limit(1), 0)

    def test_binary_limit_returns_one_for_an_input_greater_than_one_if_no_threshold_supplied(self):
        self.assertEqual(binary_limit(2), 1)
        self.assertEqual(binary_limit(3), 1)

    def test_binary_limit_returns_zero_for_an_input_that_is_less_than_or_equal_to_a_supplied_threshold(self):
        self.assertEqual(binary_limit(1, threshold=5), 0)
        self.assertEqual(binary_limit(5, threshold=5), 0)

    def test_binary_limit_returns_zero_for_an_input_that_is_greater_than_a_supplied_threshold(self):
        self.assertEqual(binary_limit(11, threshold=10), 1)

if __name__ == "__main__":
    ut.main()
