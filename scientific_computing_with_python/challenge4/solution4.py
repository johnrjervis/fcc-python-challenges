class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return "Rectangle(width=" + str(self.width) + ", height=" + str(self.height) + ")"

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def get_area(self):
        """Returns the area of the rectangle"""
        return self.width * self.height

    def get_perimeter(self):
        """Returns the perimeter of the rectangle"""
        return 2 * self.width + 2 * self.height

    def get_diagonal(self):
        """Returns the length of the diagonal of the rectangle"""
        return (self.width ** 2 + self.height ** 2) ** 0.5

    def get_picture(self):
        """Returns an ASCII-style representation of the rectangle.
           Each asterisk represents one unit of width and one unit of height.
           Returns an error message for a rectangle with width or height above 50"""

        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        else:
            return ''.join([f'{"*" * self.width}\n' for i in range(self.height)])

    def get_amount_inside(self, otherRectangle):
        """Returns the number of another rectangle instance that could fit inside this rectangle"""
        return (self.width // otherRectangle.width) * (self.height // otherRectangle.height)

class Square(Rectangle):

    def __init__(self, side_length):
        super().__init__(side_length, side_length)

    def __str__(self):
        return "Square(side=" + str(self.width) + ")"

    def set_side(self, side_length):
        """Sets_the height and width to side_length"""
        self.width = side_length
        self.height = side_length

    def set_width(self, side_length):
        """Calls set_side to set both height and width"""
        self.set_side(side_length)

    def set_height(self, side_length):
        """Calls set_side to set both height and width"""
        self.set_side(side_length)
