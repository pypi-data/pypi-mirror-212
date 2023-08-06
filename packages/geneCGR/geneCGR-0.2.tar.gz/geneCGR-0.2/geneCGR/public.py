#This is available to public
# Import necessary classes and functions from private file

from _private import Generate


#Define the same function
def square(i):


    # Make Insatnce of class imported from private file
    generator = Generate()
    # Use function from that file
    generator.square(i)

    # The core logic of function is not revealed here

def cube(i):
    generator = Generate()
    generator.cube(i)