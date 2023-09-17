import unittest as ut
from solution1 import *

class FormatSingleProblemTests(ut.TestCase):
    """Tests for the format_single_problem helper function"""

    def test_format_single_problem_returns_a_list_containing_four_strings(self):
        formatted_problem = format_single_problem("2 + 2")

        self.assertTrue(isinstance(formatted_problem, list))
        self.assertEqual(len(formatted_problem), 4)
        for elem in formatted_problem:
            self.assertTrue(isinstance(elem, str))

    def test_all_strings_in_the_list_returned_by_format_single_problem_are_the_same_length(self):
        formatted_problem = format_single_problem("2 + 2")

        for i in range(3):
            self.assertEqual(len(formatted_problem[3]), len(formatted_problem[i]))

    def test_returned_strings_are_two_chars_longer_than_the_first_supplied_operand_if_it_is_longer_than_the_second(self):
        formatted_problem = format_single_problem("12 + 2")

        for elem in formatted_problem:
            self.assertEqual(len(elem), 4)

    def test_returned_strings_are_two_characters_longer_than_the_second_operand_if_this_is_the_longest(self):
        formatted_problem = format_single_problem("12 + 200")

        for elem in formatted_problem:
            self.assertEqual(len(elem), 5)

    def test_the_first_element_of_the_returned_list_is_the_first_operand_right_justified(self):
        formatted_problem = format_single_problem("12 + 24")

        self.assertEqual(formatted_problem[0], "  12")

    def test_the_second_list_element_is_the_operator_left_justified_followed_by_the_second_operand_right_justified(self):
        formatted_problem = format_single_problem("12 + 24")

        self.assertEqual(formatted_problem[1], "+ 24")

    def test_the_third_element_consists_only_of_dashes(self):
        formatted_problem = format_single_problem("12 + 24")

        self.assertEqual(formatted_problem[2], "----")

    def test_the_fourth_element_is_the_right_justified_sum_of_the_two_operands_when_the_operator_is_the_plus_sign(self):
        formatted_problem = format_single_problem("2 + 2")

        self.assertEqual(formatted_problem[3], "  4")

    def test_the_fourth_element_is_the_right_justified_difference_of_the_operands_when_the_operand_is_a_minus_sign(self):
        formatted_problem = format_single_problem("10 - 2")

        self.assertEqual(formatted_problem[3], "   8")

    def test_an_operator_other_than_plus_or_minus_raises_a_bad_operator_exception(self):
        self.assertRaises(BadOperatorError, format_single_problem, "2 & 2")

    def test_an_operand_with_any_non_digit_characters_raises_a_bad_operand_exception(self):
        self.assertRaises(BadOperandError, format_single_problem, "2& + 2")

    def test_an_operand_longer_than_four_digits_raises_an_operand_too_long_exception(self):
        self.assertRaises(OperandTooLongError, format_single_problem, "20000 + 2")

class ArithmeticArrangerTests(ut.TestCase):
    """Tests for the arithmetic_arranger_function"""

    def test_arithmetic_arranger_returns_four_lines_of_text_when_the_second_argument_is_true(self):
        arranged_problems_lines = arithmetic_arranger(["2 + 2"], True).split('\n')

        self.assertEqual(len(arranged_problems_lines), 4)

    def test_arithmetic_arranger_returns_three_lines_of_text_when_the_second_argument_is_false(self):
        arranged_problems_lines = arithmetic_arranger(["2 + 2"], False).split('\n')

        self.assertEqual(len(arranged_problems_lines), 3)

    def test_arithmetic_arranger_returns_three_lines_of_text_when_the_second_argument_is_not_supplied(self):
        arranged_problems_lines = arithmetic_arranger(["2 + 2"]).split('\n')

        self.assertEqual(len(arranged_problems_lines), 3)

    def test_the_third_line_of_text_returned_by_arithmetic_arranger_consists_of_dashes(self):
        arranged_problems_lines = arithmetic_arranger(["2 + 2"]).split('\n')

        self.assertEqual(arranged_problems_lines[2], "---")

    def test_when_the_third_line_returned_by_arithmetic_arranger_has_a_space_is_at_the_end_when_it_is_not_the_last_line(self):
        arranged_problems_lines = arithmetic_arranger(["2 + 2"], True).split('\n')

        self.assertEqual(arranged_problems_lines[2], "--- ")

    def test_arithmetic_arranger_returns_a_single_problem_as_string_with_added_spaces_and_newline_character(self):
        arranged_problems = arithmetic_arranger(["2 + 2"], True)

        self.assertEqual(arranged_problems, "  2 \n+ 2 \n--- \n  4")

    def test_arithmetic_arranger_puts_four_spaces_between_problems(self):
        arranged_problems = arithmetic_arranger(["2 + 2", "16 - 4"], True)

        # could use regex to assert the string should match a repeating pattern?
        self.assertEqual(arranged_problems, "  2      16 \n+ 2    -  4 \n---    ---- \n  4      12")

    def test_more_than_five_problems_in_argument_list_returns_an_error(self):
        list_of_six_problems = ["1 + 1", "2 + 2", "3 + 3", "4 + 4", "5 + 5", "6 + 6"]

        self.assertEqual(arithmetic_arranger(list_of_six_problems), "Error: Too many problems.")

    def test_an_error_message_is_returned_if_format_problem_raises_a_bad_operator_exception(self):
        self.assertEqual(arithmetic_arranger(["2 * 2"]), "Error: Operator must be '+' or '-'.")

    def test_an_error_message_is_returned_if_format_problem_raises_a_bad_operand_exception(self):
        self.assertEqual(arithmetic_arranger(["2% + 2"]), "Error: Numbers must only contain digits.")

    def test_an_error_message_is_returned_if_format_problem_raises_an_operand_too_long_exception(self):
        self.assertEqual(arithmetic_arranger(["20000 + 2"]), "Error: Numbers cannot be more than four digits.")

if __name__ == "__main__":
    ut.main()
