import unittest as ut
from unittest.mock import patch, call
from solution2 import *

class ConvertTimeToMinutesTest(ut.TestCase):
    """Tests for the convert_time_to_minutes function"""

    def test_convert_time_converts_zero_time_correctly(self):
        self.assertEqual(convert_time_to_minutes("00:00"), 0)

    def test_convert_time_converts_minutes_correctly(self):
        self.assertEqual(convert_time_to_minutes("00:01"), 1)

    def test_convert_time_converts_hours_correctly(self):
        self.assertEqual(convert_time_to_minutes("01:00"), 60)

    def test_convert_time_converts_a_combination_of_hours_and_minutes_correctly(self):
        self.assertEqual(convert_time_to_minutes("02:15"), 135)

    def test_convert_time_converts_midnight_correctly(self):
        self.assertEqual(convert_time_to_minutes("00:00 AM"), 0)

    def test_convert_time_converts_midday_correctly(self):
        self.assertEqual(convert_time_to_minutes("12:00 PM"), 720)

    def test_convert_time_converts_arbitrary_afternoon_time_correctly(self):
        self.assertEqual(convert_time_to_minutes("08:21 PM"), 1221)

    def test_convert_time_returns_zero_minutes_when_the_supplied_argument_is_twelve_am(self):
        self.assertEqual(convert_time_to_minutes("12:00 AM"), 0)

    def test_convert_time_returns_correct_value_for_five_past_twelve_am(self):
        self.assertEqual(convert_time_to_minutes("12:05 AM"), 5)

class ConvertMinutesToTimeTest(ut.TestCase):
    """Tests for the convert_minutes_to_time function"""

    def test_convert_minutes_converts_hours_and_minutes_correctly(self):
        self.assertEqual(convert_minutes_to_time(85, False), "1:25 AM")

    def test_convert_minutes_converts_one_hour_correctly_and_pads_single_digit_minutes_correctly(self):
        self.assertEqual(convert_minutes_to_time(60, False), "1:00 AM")

    def test_convert_minutes_return_value_ends_with_PM_for_afternoon_times(self):
        self.assertEqual(convert_minutes_to_time(720, False)[-2:], "PM")

    def test_convert_minutes_adjusts_hours_for_afternoon_times(self):
        self.assertEqual(convert_minutes_to_time(841, False), "2:01 PM")

    def test_convert_minutes_converts_zero_minutes_to_twelve_am(self):
        self.assertEqual(convert_minutes_to_time(0, False), "12:00 AM")

    def test_convert_minutes_converts_ten_minutes_correctly(self):
        self.assertEqual(convert_minutes_to_time(10, False), "12:10 AM")

    def test_convert_minutes_does_not_adjust_midday_to_zero_hours(self):
        self.assertEqual(convert_minutes_to_time(750, False), "12:30 PM")

    def test_convert_minutes_removes_additional_days_from_time(self):
        self.assertEqual(convert_minutes_to_time(1530, False)[:4], "1:30")

    def test_convert_minutes_adds_next_day_text_where_appropriate(self):
        self.assertEqual(convert_minutes_to_time(1530, False), "1:30 AM (next day)")

    def test_convert_minutes_adds_text_for_multiple_days_later(self):
        self.assertEqual(convert_minutes_to_time(3000, False), "2:00 AM (2 days later)")

    def test_convert_minutes_adds_the_day_of_the_week_if_a_second_argument_is_supplied(self):
        self.assertEqual(convert_minutes_to_time(1, "Thursday"), "12:01 AM, Thursday")

    def test_convert_minutes_alters_day_of_the_week_for_next_day(self):
        self.assertEqual(convert_minutes_to_time(1450, "Friday"), "12:10 AM, Saturday (next day)")

    def test_convert_minutes_wraps_the_weekday_round_to_the_start_of_the_week_when_necessary(self):
        self.assertEqual(convert_minutes_to_time(1600, "Sunday"), "2:40 AM, Monday (next day)")

    def test_convert_minutes_is_forgiving_of_weekday_arguments_with_random_capitalisation(self):
        self.assertEqual(convert_minutes_to_time(1000, "weDnesDaY"), "4:40 PM, Wednesday")

class AddTimeTest(ut.TestCase):

    # assert called with using mocks?
    @patch('solution2.convert_minutes_to_time')
    @patch('solution2.convert_time_to_minutes')
    def test_add_time_calls_convert_time_to_minutes_with_the_two_supplied_arguments(self, mock_convert_time_to_minutes, mock_convert_minutes_to_time):
        add_time("01:30 AM", "00:15")

        self.assertTrue(mock_convert_time_to_minutes.called)
        self.assertEqual(mock_convert_time_to_minutes.call_count, 2)
        # the second call to mock_convert_time_to_minutes sets the call_args property to "00:15" (so "01:30 AM" is lost) 
        self.assertEqual(mock_convert_time_to_minutes.call_args_list[0], call("01:30 AM"))
        self.assertEqual(mock_convert_time_to_minutes.call_args_list[1], call("00:15"))

    @patch('solution2.convert_minutes_to_time')
    def test_add_time_calls_convert_minutes_to_time_with_the_sum_of_the_two_convert_minutes_to_time_return_values(self, mock_convert_minutes_to_time):
        self.assertEqual(convert_time_to_minutes("01:30 AM") + convert_time_to_minutes("00:15"), 105)

        add_time("01:30 AM", "00:15")

        self.assertTrue(mock_convert_minutes_to_time.called)
        self.assertEqual(mock_convert_minutes_to_time.call_args, call(105, False))

    @patch('solution2.convert_minutes_to_time')
    def test_add_time_passes_weekday_argument_to_convert_minutes_to_time(self, mock_convert_minutes_to_time):
        add_time("01:30 AM", "00:15", "Thursday")

        self.assertTrue(mock_convert_minutes_to_time.called)
        self.assertEqual(mock_convert_minutes_to_time.call_args, call(105, "Thursday"))

    def test_add_time_returns_a_properly_formatted_time(self):
        self.assertEqual(add_time("0:10 AM", "0:00"), "12:10 AM")

    def test_add_time_updates_hour_when_the_duration_is_one_hour(self):
        self.assertEqual(add_time("0:10 AM", "1:00"), "1:10 AM")

    def test_add_time_updates_minutes_when_the_minutes_total_is_less_than_60(self):
        self.assertEqual(add_time("0:00 AM", "0:10"), "12:10 AM")

    def test_add_time_formats_minutes_as_two_characters_even_when__minutes_are_less_than_10(self):
        self.assertEqual(add_time("0:00 AM", "0:05"), "12:05 AM")

    def test_add_time_increases_hours_when_total_minutes_are_greater_than_60(self):
        self.assertEqual(add_time("0:30 AM", "0:45"), "1:15 AM")

    def test_add_time_includes_next_day_text_where_appropriate(self):
        self.assertEqual(add_time("11:30 PM", "0:45"), "12:15 AM (next day)")

if __name__ == "__main__":
    ut.main()
