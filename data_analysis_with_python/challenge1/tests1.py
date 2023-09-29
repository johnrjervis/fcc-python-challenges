import unittest as ut
#from io import StringIO
#import sys
from solution1 import *

class calculate_tests(ut.TestCase):
    """Tests for the calculate function"""

    def setUp(self):
        self.REQUIRED_KEYS = ["mean", "variance", "standard deviation", "max", "min", "sum"]
        self.example_result= calculate([i for i in range(9)])

    def test_calculate_returns_a_dict(self):
        self.assertTrue(isinstance(self.example_result, dict))

    def test_dict_returned_by_calculate_contains_six_specified_keys(self):
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, self.example_result)

    def test_dict_value_for_each_of_the_required_keys_is_a_list_in_returned_dict(self):
        for key in self.REQUIRED_KEYS:
            self.assertTrue(isinstance(self.example_result[key], list))

    def test_all_values_in_the_dict_contain_three_elements(self):
        for key in self.REQUIRED_KEYS:
            self.assertTrue(len(self.example_result[key]), 3)

    def test_the_first_element_in_the_mean_list_contains_the_averages_of_the_three_columns_of_the_rearranged_array(self):
        # Expected results are taked from the result that  freeCodeCamp provide for the example array
        # see https://www.freecodecamp.org/learn/data-analysis-with-python/data-analysis-with-python-projects/mean-variance-standard-deviation-calculator
        self.assertEqual(self.example_result["mean"][0], [3.0, 4.0, 5.0])

    def test_the_second_mean_list_element_contains_the_averages_of_the_rearranged_array_rows(self):
        self.assertEqual(self.example_result["mean"][1], [1.0, 4.0, 7.0])

    def test_the_final_mean_list_element_is_the_average_of_the_entire_input_list(self):
        self.assertEqual(self.example_result["mean"][2], 4.0)

    def test_the_variance_list_contains_the_variance_of_the_columns_and_rows_of_the_rearragned_array_and_of_the_input_list(self):
        self.assertEqual(self.example_result["variance"], [[6.0, 6.0, 6.0], [0.6666666666666666, 0.6666666666666666, 0.6666666666666666], 6.666666666666667])

    def test_the_result_includes_the_standard_deviations_of_the_rearranged_rows_and_columns_and_the_input_list(self):
        self.assertEqual(self.example_result["standard deviation"], [[2.449489742783178, 2.449489742783178, 2.449489742783178], [0.816496580927726, 0.816496580927726, 0.816496580927726], 2.581988897471611])

    def test_the_result_includes_the_maximum_values_of_the_rearranged_rows_and_columns_and_the_input_list(self):
        self.assertEqual(self.example_result["max"], [[6, 7, 8], [2, 5, 8], 8])
    
    def test_the_result_includes_the_minimum_values_of_the_rearranged_rows_and_columns_and_the_input_list(self):
        self.assertEqual(self.example_result["min"], [[0, 1, 2], [0, 3, 6], 0])

    def test_the_result_includes_the_sums_of_the_rearranged_rows_and_columns_and_the_input_list(self):
        self.assertEqual(self.example_result["sum"], [[9, 12, 15], [3, 12, 21], 36])

    def test_calculate_raises_a_value_error_exception_if_the_input_list_contains_less_than_nine_numbers(self):
        self.assertRaises(ValueError, calculate, [i for i in range(8)])

    def test_calculate_value_error_exception_message_is_list_must_contain_nine_numbers_if_input_list_is_too_short(self):
        with self.assertRaises(Exception) as context:
            calculate([i for i in range(8)])

        self.assertEqual(str(context.exception), "List must contain nine numbers.")

    def test_calculate_excludes_values_after_the_ninth_element_if_the_input_list_is_too_long(self):
        self.maxDiff = None
        self.assertEqual(self.example_result, calculate([i for i in range(10)]))


if __name__ == "__main__":
  ut.main()
