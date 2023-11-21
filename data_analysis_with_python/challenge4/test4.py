import unittest as ut
from solution4 import convert_month_number_to_name

class ConvertMonthNumberToNameTests(ut.TestCase):
    """Tests for the convert_month_number_to_main function"""

    def test_convert_month_number_to_main_returns_the_correct_month_names_for_a_range_of_inputs(self):
        self.assertEqual(convert_month_number_to_name(1), "January")
        self.assertEqual(convert_month_number_to_name(6), "June")
        self.assertEqual(convert_month_number_to_name(9), "September")

if __name__ == "__main__":
    ut.main()
