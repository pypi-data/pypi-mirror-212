"""
Example document to provide quick overwiev on how to use this package
"""

# Import the Main file
import Shapes as sh

# a) Create a Triangle and perform simple operations

My_triangle = sh.Triangle([[1,1],[3,1],[4,3]])
print(My_triangle)
print("Perimeter of this triangle is " + str(My_triangle.perimeter()))

# b) Check if two circles intersect

Circle_1 = sh.Circle(2) # Circle with radius of 2 and center at (0,0)
Circle_2 = sh.Circle(3,(3,0.2)) # Circle with radious of 3 and center at (3,0.2)

print(Circle_1.intersect(Circle_2))



# Additional: Use provided functions

