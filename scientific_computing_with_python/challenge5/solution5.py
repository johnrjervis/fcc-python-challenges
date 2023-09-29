import copy, random

class Hat:

    def __init__(self, **kwargs):
        self.contents = self.populate_contents(kwargs)

    def populate_contents(self, kwargs_dict):
        """Converts the arguments dict into a list of colours.
           The colours are equal to the dict key,
           and each colour is repeated by the number of times specified by the corresponding dict value"""
        return [key for key in kwargs_dict.keys() for i in range(kwargs_dict[key])]

    def draw(self, number_of_balls):
        """Returns a list of randomly drawn balls of length equal to number_of_balls
           if number_of_balls is greater than the number of balls in the hat, the hat's contents are returned.
           Balls are removed from the hat as they are added to the list of balls drawn"""
        result = []

        if number_of_balls >= len(self.contents):
            for ball in self.contents:
                result.append(ball)
            self.contents = []
        else:
            for i in range(number_of_balls):
                random_index = random.randint(0, len(self.contents) - 1)
                result.append(self.contents[random_index])
                del(self.contents[random_index])

        return result

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    """Conducts experiments to see whether the expected_balls dict is matched in a draw of num_balls from a hat object
       The experiment is repeated num_experiments times, and the probability of a match is returned as the fraction of experiments in which a match is achieved"""

    successful_matches = 0

    for i in range(num_experiments):

        hatCopy = copy.deepcopy(hat)
        draw_result = hatCopy.draw(num_balls_drawn)
        expected_colours_matched = []

        for colour in expected_balls.keys():
            if draw_result.count(colour) >= expected_balls[colour]:
                expected_colours_matched.append(True)
            else:
                expected_colours_matched.append(False)
                break

        if (all(expected_colours_matched)):
            successful_matches += 1

    return successful_matches / round(num_experiments, 2)
