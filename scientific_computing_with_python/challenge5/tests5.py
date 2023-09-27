import unittest as ut
from solution5 import *
import copy

class HatTests(ut.TestCase):
    """Tests for the Hat class"""

    def test_hat_with_one_argument_has_contents_list_containing_a_string_equal_to_the_supplied_colour(self):
        newHat = Hat(purple=1)

        self.assertEqual(newHat.contents, ["purple"])

    def test_hat_contents_can_be_populated_with_single_balls_of_different_colours(self):
        newHat = Hat(purple=1, red=1, orange=1)
        newHat.contents.sort()

        self.assertEqual(newHat.contents, ["orange", "purple", "red"])

    def test_hat_contents_can_be_populated_with_multiple_balls_of_the_same_colour(self):
        newHat = Hat(blue=3)

        self.assertEqual(newHat.contents, ["blue", "blue", "blue"])

    def test_a_ball_can_be_drawn_from_a_hat(self):
        newHat = Hat(red=1, blue=1)

        draw = newHat.draw(1)

        self.assertEqual(len(draw), 1)
        self.assertIn(draw, [["red"], ["blue"]])

    def test_the_number_of_balls_in_a_hat_decreases_by_one_when_a_ball_is_drawn(self):
        newHat = Hat(red=1, blue=1)
        self.assertEqual(len(newHat.contents), 2)

        newHat.draw(1)

        self.assertEqual(len(newHat.contents), 1)

    def test_the_drawn_ball_is_different_from_the_ball_that_is_left_in_the_hat(self):
        newHat = Hat(red=1, blue=1)

        draw = newHat.draw(1)

        self.assertIn(draw, [["red"], ["blue"]])
        self.assertIn(newHat.contents, [["red"], ["blue"]])
        self.assertNotEqual(draw, newHat.contents)

    def test_multiple_balls_of_the_same_colour_can_be_drawn_from_a_hat(self):
        newHat = Hat(blue=5)

        draw = newHat.draw(3)

        self.assertEqual(draw, ["blue", "blue", "blue"])

    def test_balls_that_are_not_drawn_are_left_in_the_hat(self):
        newHat = Hat(blue=5)

        draw = newHat.draw(3)

        self.assertEqual(newHat.contents, ["blue", "blue"])

    def test_multiple_balls_can_be_drawn_from_a_hat(self):
        newHat = Hat(blue=1, green=1, orange=1)

        draw = newHat.draw(2)
        draw.sort()

        self.assertIn(draw, [["blue", "green"], ["blue", "orange"], ["green", "orange"]])

    def test_all_balls_can_be_drawn_from_a_hat(self):
        newHat = Hat(blue=1, green=1, orange=1)

        draw = newHat.draw(3)

        draw.sort()
        self.assertEqual(draw, ["blue", "green", "orange"])

    def test_an_attempt_to_draw_more_balls_than_are_in_a_hat_returns_all_balls(self):
        newHat = Hat(blue=1, green=1, orange=1)

        draw = newHat.draw(5)

        draw.sort()
        self.assertEqual(draw, ["blue", "green", "orange"])

    def test_a_draw_taken_after_all_balls_have_already_been_drawn_from_a_hat_returns_an_empty_list(self):
        newHat = Hat(blue=1, green=1, orange=1)

        draw1 = newHat.draw(3)
        draw2 = newHat.draw(3)

        self.assertEqual(len(draw1), 3)
        self.assertEqual(len(draw2), 0)

    def test_draws_from_a_hat_are_random(self):
        newHat = Hat(blue=2, red=2, orange=2, green=2, yellow=2, pink=2, purple=2)
        newHatCopy = copy.deepcopy(newHat)

        draw1 = newHat.draw(10)
        draw2 = newHatCopy.draw(10)

        self.assertNotEqual(draw1, draw2)

class ExperimentTests(ut.TestCase):
    """Tests for the experiment function"""

    def test_experiment_returns_a_probability_of_zero_when_the_expected_colour_ball_is_not_in_the_hat(self):
        newHat = Hat(blue=1)

        self.assertEqual(experiment(hat=newHat, expected_balls={"red": 1}, num_balls_drawn=1, num_experiments=1), 0)

    def test_experiment_returns_one_when_the_expected_colour_is_the_colour_of_the_only_ball_in_the_hat(self):
        newHat = Hat(blue=1)

        self.assertEqual(experiment(newHat, {"blue": 1}, 1, 1), 1)

    def test_experiment_returns_zero_when_the_number_expected_is_more_than_the_number_drawn(self):
        newHat = Hat(blue=2)

        self.assertEqual(experiment(newHat, {"blue": 2}, 1, 1), 0)

    def test_experiment_returns_zero_when_the_number_expected_for_one_colour_is_more_than_the_number_of_that_colour_in_the_hat(self):
        newHat = Hat(blue=3, red=2, orange=1, green=2)

        self.assertEqual(experiment(newHat, {"orange": 2}, 8, 1), 0)

    def test_experiment_returns_one_when_the_all_expected_colours_are_guaranteed_to_match(self):
        newHat = Hat(blue=2, red=2, orange=2, green=2)

        self.assertEqual(experiment(newHat, {"blue": 2, "orange": 2,"red": 2, "green": 2}, 8, 1), 1)

    def test_multiple_experiments_for_a_guaranteed_match_returns_a_result_of_one(self):
        newHat = Hat(red=1)

        self.assertEqual(experiment(hat=newHat, expected_balls={"red": 1}, num_balls_drawn=1, num_experiments=10000), 1)

    def test_multiple_experiments_for_a_guaranteed_non_match_returns_a_result_of_zero(self):
        newHat = Hat(red=1)

        self.assertEqual(experiment(hat=newHat, expected_balls={"blue": 1}, num_balls_drawn=1, num_experiments=10000), 0)

    def test_multiple_experiments_return_neither_one_nor_zero_for_a_small_number_of_repeat_experiments(self):
        newHat = Hat(red=1, blue=1)

        result = experiment(newHat, {"blue": 1}, 1, 20)

        self.assertNotEqual(result, 0)
        self.assertNotEqual(result, 1)

    def test_result_tends_towards_the_correct_value_for_a_large_number_of_repeat_experiments(self):
        newHat = Hat(red=1, blue=1)

        self.assertAlmostEqual(
            experiment(
                hat=newHat,
                expected_balls={"blue": 1},
                num_balls_drawn=1,
                num_experiments=10000),
            0.5, 1)

if __name__ == "__main__":
    ut.main()
