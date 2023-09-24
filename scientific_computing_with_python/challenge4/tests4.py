import unittest as ut
from solution4 import *
from io import StringIO
import sys

class RectangleTests(ut.TestCase):
    """Tests for the Rectangle Class"""

    def test_Rectangle_initialises_with_width_and_height_properties(self):
        newRectangle = Rectangle(4, 5)

        self.assertEqual(newRectangle.width, 4)
        self.assertEqual(newRectangle.height, 5)


    def test_the_set_width_method_sets_the_width_of_an_instance_of_Rectangle(self):
        newRectangle = Rectangle(4, 5)

        newRectangle.set_width(3)

        self.assertEqual(newRectangle.width, 3)


    def test_set_height_sets_the_height_of_a_Rectangle(self):
        newRectangle = Rectangle(1, 2)

        newRectangle.set_height(3)

        self.assertEqual(newRectangle.height, 3)

    def test_the_get_area_method_returns_the_product_of_the_height_and_width_of_a_Rectangle(self):
        newRectangle = Rectangle(4, 5)

        self.assertEqual(newRectangle.get_area(), 20)

    def test_the_get_perimeter_method_returns_the_sum_of_twice_the_height_and_twice_the_width_of_a_Rectangle(self):
        newRectangle = Rectangle(4, 5)

        self.assertEqual(newRectangle.get_perimeter(), 18)

    def test_the_get_diagonal_method_returns_the_length_of_the_diagonal_of_a_Rectangle(self):
        newRectangle1 = Rectangle(3, 4)
        newRectangle2 = Rectangle(5, 7)

        self.assertEqual(newRectangle1.get_diagonal(), 5)
        self.assertEqual(newRectangle2.get_diagonal(), (5 ** 2 + 7 ** 2) ** 0.5)

    def test_get_picture_prints_a_series_of_asterisks_that_represent_a_rectangle(self):
        newRectangle = Rectangle(5, 3)

        self.assertEqual(newRectangle.get_picture(), "*****\n*****\n*****\n")

    def test_get_picture_prints_an_error_message_for_a_rectangle_with_width_greater_than_50(self):
        newRectangle = Rectangle(51, 3)

        self.assertEqual(newRectangle.get_picture(), "Too big for picture.")

    def test_get_picture_prints_an_error_message_for_a_rectangle_with_height_greater_than_50(self):
        newRectangle = Rectangle(2, 53)

        self.assertEqual(newRectangle.get_picture(), "Too big for picture.")

    def test_the_get_amount_inside_returns_the_number_of_another_Rectangle_that_can_fit_inside_the_current_Rectangle(self):
        bigRectangle = Rectangle(14, 9)
        mediumRectangle = Rectangle(4, 3)
        littleRectangle = Rectangle(2, 3)

        self.assertEqual(bigRectangle.get_amount_inside(mediumRectangle), 9)
        self.assertEqual(bigRectangle.get_amount_inside(littleRectangle), 21)

    def test_printing_a_rectangle_provides_an_appropriate_description_that_includes_height_and_width(self):
        newRectangle = Rectangle(4, 2)
        captured_output = StringIO()
        sys.stdout = captured_output

        print(newRectangle)

        self.assertEqual(captured_output.getvalue(), "Rectangle(width=4, height=2)\n")


class SquareTests(ut.TestCase):
    """Tests for the Square Class"""

    def test_square_object_is_an_instance_of_a_rectangle(self):
        self.assertTrue(isinstance(Square(1), Rectangle))

    def test_an_instance_of_square_has_width_and_height_properties_that_are_equal_to_the_single_argument(self):
        newSquare = Square(5)

        self.assertEqual(newSquare.width, 5)
        self.assertEqual(newSquare.width, newSquare.height)

    def test_an_instance_of_square_has_access_to_the_methods_of_the_Rectangle_class(self):
        newSquare = Square(5)
        littleSquare = Square(2)
        littleRectangle = Rectangle(3, 2)

        self.assertEqual(newSquare.get_area(), 25)
        self.assertEqual(newSquare.get_perimeter(), 20)
        self.assertEqual(newSquare.get_diagonal(), (2 * 5 **2) ** 0.5)
        self.assertEqual(newSquare.get_amount_inside(littleSquare), 4)
        self.assertEqual(newSquare.get_amount_inside(littleRectangle), 2)
        self.assertEqual(newSquare.get_picture(), "*****\n*****\n*****\n*****\n*****\n")

    def test_the_set_side_method_should_set_the_height_and_width_to_the_same_value(self):
        newSquare = Square(5)

        newSquare.set_side(4)

        self.assertEqual(newSquare.height, 4)
        self.assertEqual(newSquare.width, newSquare.height)

    def test_the_set_width_method_sets_the_width_and_height_of_a_square_from_a_single_argument(self):
        newSquare = Square(5)

        newSquare.set_width(4)

        self.assertEqual(newSquare.height, 4)
        self.assertEqual(newSquare.width, newSquare.height)

    def test_the_set_height_method_also_sets_the_width_and_height_of_a_square(self):
        newSquare = Square(5)

        newSquare.set_height(4)

        self.assertEqual(newSquare.height, 4)
        self.assertEqual(newSquare.width, newSquare.height)

    def test_printing_a_square_provides_an_appropriate_description_that_includes_the_side_length(self):
        newSquare = Square(2)
        captured_output = StringIO()
        sys.stdout = captured_output

        print(newSquare)

        self.assertEqual(captured_output.getvalue(), "Square(side=2)\n")

if __name__ == "__main__":
    ut.main()
