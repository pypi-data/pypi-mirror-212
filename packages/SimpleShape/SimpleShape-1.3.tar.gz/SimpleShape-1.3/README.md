# README

This project enables the creation of different geometric objects, on which we can perform different operations, like calculation of their perimeter.

## Features

- Create and visualise various geometric objects: Triangle, Rectangle, Polygon, Circle and Ellipse
- Calculate their perimeter and their area
- Check if two objects intersect
- Save and load geometric objects to and from JSON files

## Installation

Download and expand the zip (.whl) file and insert the SimpleShape.py function, located in the SimpleShape subfolder, to location of your python document, or use **pip install SimpleShape**. Then, write **import SimpleShape** in your python document to begin using the package.

## 1. Instructions

To start using this project, create the Geometric object with available classes and perform different methods (see section 1.1). You can also check example.py, located in the SimpleShape subfolder, for a quick overwiev on how to use this package.

This package also provides various functions that are described in section 1.2.

### 1.1 Geometric Classes and Methods

##### Class Geometry(coordinates): 

Parent class for creating geometric objects. Here, coordinates is 2-D array of arrays that represent coordinates in x-y plane (one example being coordinates = [(0,0), (2,0), (4,4), (0,4)]). In case of Ellipse and Circle, different parameters are inserted (see below), for example the coordinates of their center.

###### Parent class has following methods:

- \_\_init__(self, coordinates): Initialization method for the object.
- \_\_str__(self) -> str: String representation of the object, obtained using print(object)
- perimeter(self) -> float: Returns the perimeter of the geometric object
- area(self) -> float: Returns the area of the geometric object
- intersect(self, other) -> bool: Check if two objects intersect. Note that tangency also counts as intersection
- visualize(self): Visualize the object using matplotlib module

Aside from these methods, there are various functions to convert geometric objects to and from JSON format. See section 1.2 for more details.

##### Class Triangle(coordinates):

A class for creating triangles using three points (f.e. [(0,0), (2,0), (4,4)]).

##### Class Rectangle(coordinates):

A class for creating rectangles using four points that need to be inserted in clockwise or counter-clockwise order. 

##### Class Polygon(coordinates):

A class for creating polygons using three or more points that need to be inserted in fixed order. If the polygon is self-intersecting, the area() method does not return correct values.

##### Class Circle(r, center = (0, 0)):

A class for creating circles. Here, r is radius (r > 0) and center (default value (0,0)) represents center of the circle on x-y plane. 

##### Class Ellipse(a, b, f = 0, center = (0, 0)):

A class for creating ellipses. Here, a is the major axis, b is the minor axis (a,b > 0), f is the rotation in counter-clockwise direction (in degrees, default value 0) and center represents center of ellipse on x-y plane (default value (0,0)). 

### 1.2 Functions

This package contains functions for working with JSON data as well as other functions that perform different operations on geometric objects.

##### JSON functions:

- **to_json(self) -> json**: Convert the geometric object to .JSON format
- **from\_json(json\_data) -> object**: Create a geometric object from JSON data
- **save_shapes(shapes, filename)**: Save json_data (shapes) to file (filename)
- **load_shapes(filename):** Load json_data from a file (filename)

##### Other functions:

- **random_shape(shape)**: Create a geometric object of random dimensions. If the shape parameter is not specified, an arbitrary geometric object will be returned. Otherwise, insert one of the following as an argument: "Rectangle", "Triangle", "Circle", "Ellipse", "Polygon".
- **rotate(P1, P2, f)**: Rotate point P1 (x1,y1) around point P2 (x2,y2) for angle f in radians.        
- **intersect(A,B,C,D)**: Check if two line segments (AB and CD, where each capital letter represents a point (x, y) on x-y plane) intersect
- **parallel(A,B,C,D)**: Check if two line segments (AB and CD, where each capital letter represents a point (x, y) on x-y plane) are parallel
- **Line_Intersect_Circle(A, B, c, r)**: Check if line segment AB intersect a circle with radius r > 0 and central point c (x, y).

**Note: Tangency is also considered an intersection!**