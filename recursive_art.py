""" TODO: Put your header comment here """

import random
import math
from PIL import Image

func = ["sqrt", "sqr","cos_pi", "sin_pi","opp","exp","prod", "avg", "xf","yf"]
def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    drange = random.randint(0,max_depth-min_depth)
    if max_depth == 0 or (drange + min_depth) == 0:
        decide = random.randint(1,2)
        if decide == 1:
            return "x"
        else:
            return "y"
    else:
        min_depth = min_depth - 1
        max_depth = max_depth - 1
        func_index = random.randint(0, 9)
        if func_index  > 4:
            return [func[func_index], build_random_function(min_depth, max_depth), build_random_function(min_depth, max_depth)]
        else:
            return [func[func_index], build_random_function(min_depth, max_depth)]



def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    #base case
    if f[0] == "x":
        return x
    if f[0] == "y":
        return y

    #all the other cases
    if f[0] == "xf":
        return evaluate_random_function(f[1], x, y)
    elif f[0] == "yf":
        return evaluate_random_function(f[2], x, y)
    elif f[0] == "cos_pi":
        return math.cos(evaluate_random_function(f[1], x, y)*math.pi)
    elif f[0] == "sin_pi":
        return math.sin(evaluate_random_function(f[1], x, y)*math.pi)
    elif f[0] == "opp":
        return -evaluate_random_function(f[1], x, y)
    elif f[0] == "exp":
        return math.exp(evaluate_random_function(f[1], x, y)) - 1
    elif f[0] == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))/2
    elif f[0] == "sqrt":
        return math.sqrt(math.fabs(evaluate_random_function(f[1], x, y)))
    elif f[0] == "sqr":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[1], x, y)

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(6, 5, 10, 0, 1)
        0.2
        >>> remap_interval(5, 5, 10, 0, 1)
        0.0
        >>> remap_interval(10, 5, 10, 0, 1)
        1.0
    """
    scale = (output_interval_end - output_interval_start)/(input_interval_end - input_interval_start)
    shift = output_interval_start
    dif = val - input_interval_start
    new_val = (dif *scale) + shift
    return new_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart23.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
