"""
Main document with definitions of classes, methods, and functions
"""

# Import libraries

import json
from math import pi, sqrt, sin, cos
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse as _Ellipse
import numpy as np

# Parent Class

class Geometry:
    """Parent class for creating geometric objects"""
    
    def __init__(self, coordinates):
        """Initialization of the object. Somewhat different for
        circle and ellipse"""
        self.type = self.__class__.__name__
        self.coordinates = coordinates

        for element in self.coordinates:
            if len(element) != 2:
                raise Warning("Provide 2 elements for each point")
    
    def __str__(self) -> str:
        """A string representation of the object"""
        return ("The coordinates of the " + self.__class__.__name__ + " are " + 
        str(self.coordinates))

    def perimeter(self) -> float:
        """Perimeter (circumference) of the object"""
        l = 0
        for i in range(len(self.coordinates)):
            l += sqrt((self.coordinates[i][0] - self.coordinates[i-1][0])**2 +
                      (self.coordinates[i][1] - self.coordinates[i-1][1])**2)
        return l
    
    def area(self) -> float:
        """Area of object using shoelace formula"""
        s = 0
        for i in range(len(self.coordinates)):             
            s += (self.coordinates[i-1][0] * self.coordinates[i][1] -
                  self.coordinates[i][0] * self.coordinates[i-1][1])
        return abs(s/2)
            
    
    def intersect(self, other) -> bool:
        """Check if there is an intersection. This includes tangency"""
        if self.__class__.__name__ in ('Triangle','Rectangle','Polygon'):
            if other.__class__.__name__ in ('Triangle','Rectangle','Polygon'):
                for i in range(len(self.coordinates)):
                    for j in range(len(other.coordinates)):
                        if intersect(self.coordinates[i-1],self.coordinates[i],
                                     other.coordinates[j-1],other.coordinates[j]):
                            return True
                return False
            elif isinstance(other, Circle):
                for i in range(len(self.coordinates)):
                    if Line_Intersect_Circle(self.coordinates[i-1], self.coordinates[i], other.center, other.r):
                        return True
                return False
            
            elif isinstance(other, Ellipse):
                return "This feature has yet to be implemented"
            else:
                raise Warning("Invalid shape type for intersection check")
            
        
       
        elif self.__class__.__name__ == ('Circle'):
            if isinstance(other, Circle):
                distance = sqrt((self.center[0]-other.center[0])**2+
                            (self.center[1]-other.center[1])**2)
                if distance > abs(self.r - other.r): 
                    return distance <= (self.r + other.r)
                return False
            elif other.__class__.__name__ in ('Triangle','Rectangle','Polygon'):
                for i in range(len(other.coordinates)):
                    if Line_Intersect_Circle(other.coordinates[i-1], other.coordinates[i], self.center, self.r):
                        return True
                return False
            elif isinstance(other, Ellipse):
                return "This feature has yet to be implemented"
            else:
                raise Warning("Invalid shape type for intersection check")

    
        elif self.__class__.__name__ == ('Ellipse'):
            return "This feature has yet to be implemented"
        else:
            raise Warning("Invalid shape type for intersection check")
            
    
    def visualize(self) -> None:
        """Visualize the object using Matplotlib module"""
        X = np.array(self.coordinates)
        plt.figure()
        plt.scatter(X[:, 0], X[:, 1], s = 20)
        t1 = plt.Polygon(X[:,:])
        plt.gca().add_patch(t1)
        plt.show()

# Child classes (Triangle, Rectangle, Polygon, Circle, Ellipse)

class Triangle(Geometry):
    
    def __init__(self, coordinates):
        super().__init__(coordinates)

        self.a = coordinates[0]
        self.b = coordinates[1]
        self.c = coordinates[2]

        if (len(self.coordinates) != 3):
            raise Warning("Provide a 3x2 array or tuple")
        if parallel(self.a,self.b,self.b,self.c):
            raise Warning("Not a triangle. Try again") 
        if (self.a in (self.b, self.c) or self.b == self.c):
            raise Warning("Not a triangle. Try again")

    
    
class Rectangle(Geometry):
    """Insert points in clockwise or counter-clockwise direction"""
    def __init__(self, coordinates):
        super().__init__(coordinates)
        self.a = coordinates[0]
        self.b = coordinates[1]
        self.c = coordinates[2]
        self.d = coordinates[3]

        self.ab = (self.a[0]-self.b[0],self.a[1]-self.b[1])
        self.bc = (self.b[0]-self.c[0],self.b[1]-self.c[1])
        self.cd = (self.c[0]-self.d[0],self.c[1]-self.d[1])
        self.da = (self.d[0]-self.a[0],self.d[1]-self.a[1])
        
        self.ac = sqrt((self.a[0]-self.c[0])**2+(self.a[1]-self.c[1])**2)
        self.bd = sqrt((self.b[0]-self.d[0])**2+(self.b[1]-self.d[1])**2)

        eps = 1e-8
        if (len(self.coordinates) != 4):
            raise Warning("Provide a 4x2 array or tuple")
        if (self.ab[0]+self.cd[0]>eps or self.bc[0]+self.da[0]>eps or self.ac-self.bd>eps):
            raise Warning('Not a rectangle. Try again')
        if (self.ab[1]+self.cd[1]>eps or self.bc[1]+self.da[1]>eps):
            raise Warning('Not a rectangle. Try again')
        if self.a in (self.b, self.c, self.d):
            raise Warning("Not a rectangle. Try again")
        if (self.b in (self.c, self.d) or self.c == self.d):
            raise Warning("Not a rectangle. Try again")
            
class Polygon(Geometry):
    """Insert coordinates in specific order"""
    def __init__(self, coordinates):
        super().__init__(coordinates)

        if len(self.coordinates) < 3:
            raise Warning("Provide a nx2 array or tuple, where n > 2")
        # Check for parallelism
        for i in range(len(self.coordinates)):
            if parallel(self.coordinates[i-1],self.coordinates[i],
                         self.coordinates[i-2],self.coordinates[i-1]):
                raise Warning("One of the edges in polygon is 180°. Try again")
        # Check if polygon is self intersectiong
        self.is_intersected = 0
        for i in range(1, len(self.coordinates)):
            if self.is_intersected == 1: break
            for j in range(i-1): # To not consider neighbours
                if intersect(self.coordinates[i-1],self.coordinates[i],
                             self.coordinates[j-1],self.coordinates[j]):
                    if i - j != len(self.coordinates)-1: # To not consider last and first element together
                        self.is_intersected = 1
                        print("This polygon is not a simple polygon. The result of area() method will presumably be incorrect")
                        break

       
                        
class Circle(Geometry):
    
    def __init__(self, r, center = (0,0)):
        self.type = self.__class__.__name__
        self.r = r
        self.center = center
        
        if r <= 0: raise Warning("Radius is 0 or less. Use another radius")
        if len(self.center) != 2: raise Warning("Use a center point with two dimensions")
    
    def __str__(self):
        return ("Circle with radius " + str(self.r) + " and center in " +
                str(self.center)) 

    def area(self):
        """pi * r**2"""
        return pi * self.r**2

    def perimeter(self):
        """2 * pi * r"""
        return 2 * pi * self.r
           
           
    def visualize(self):
        circle=plt.Circle(self.center, self.r)
        fig, ax = plt.subplots()
        ax.set_xlim((self.center[0]-1.1*self.r, self.center[0]+self.r*1.1))
        ax.set_ylim((self.center[1]-1.1*self.r, self.center[1]+self.r*1.1))
        ax.add_patch(circle)
        plt.show()

    
class Ellipse(Geometry):
    def __init__(self, width, height, f = 0, center = (0,0)):
        self.type = self.__class__.__name__
        self.width = width
        self.height = height
        self.f = f
        self.center = center

        if self.width <= 0: raise Warning("Width is 0 or less. Use another width")
        if self.height <= 0: raise Warning("Height is 0 or less. Use another height")
        if len(self.center) != 2: raise Warning("Use a center point with two dimensions")
        
    def __str__(self):
        return ("Ellipse with width = " + str(self.width) + ", height = " + str(self.height) +
                ", rotation of " + str(self.f) + "° and center at " + str(self.center)) 

    def area(self):
        """pi * width * height"""
        return pi * self.width * self.height

    def perimeter(self):
        """Approximate calculation using Ramanujan formula"""
        return pi * (3*(self.width+self.height) - 
                     sqrt((3*self.width + self.height) * (self.width + 3 * self.height)))
           
    def visualize(self):
        fig, ax = plt.subplots()

        ax.axis('equal')
        ell = _Ellipse(xy=self.center, width=self.width, height=self.height, angle=self.f
                       , lw=4)
        
        ax.add_artist(ell)
        
        temp = max(self.width,self.height)
        ax.set_xlim((self.center[0]-1.1*temp, self.center[0]+temp*1.1))
        ax.set_ylim((self.center[1]-1.1*temp, self.center[1]+temp*1.1))
        
        plt.show()


# JSON functions

def to_json(object_list):
    """Convert the list of objects to JSON string using object attributes"""
    return json.dumps([obj.__dict__ for obj in object_list])
    
def save_shapes(json_data, filename):
    """Write JSON string to a .json file"""
    with open(filename, 'w') as outfile:
        outfile.write(json_data)
        
def load_shapes(filename):
    """Create JSON string from a .json file"""
    with open(filename, 'r') as file:
        json_data = json.load(file)
    return json_data 
        

def from_json(json_data):
    """Create a list of objects from a JSON string"""
    object_list = []
    for element in json_data:
        if element['type'] == 'Triangle':
            object_list.append(Triangle(element['coordinates']))
        elif element['type'] == 'Rectangle':
            object_list.append(Rectangle(element['coordinates']))
        elif element['type'] == 'Polygon':
            object_list.append(Polygon(element['coordinates']))
        elif element['type'] == 'Circle':
            object_list.append(Circle(element['r'], element['center']))
        elif element['type'] == 'Ellipse':
            object_list.append(Ellipse(element['width'],element['height'],
                           element['f'], element['center']))
        else:
            print('Invalid JSON data. Will not be used to create an object')
    return object_list

# Other functions

def random_shape(shape = next(iter({"Rectangle", "Triangle", "Circle", "Ellipse", "Polygon"}))):
    
    if shape == "Triangle":
        a,b,c = np.random.uniform(-1000, 1000,(3,2))
        return Triangle(([a[0],a[1]],[b[0],b[1]],[c[0],c[1]]))
    elif shape == "Rectangle":
        [a, b] = np.random.uniform(-1000,1000, 2)
        _min = min(a,b)
        _max = max(a,b)
        avg = (_min+_max)/2
        center=(avg,avg)
        f = 2*pi*np.random.uniform(0,1) # Radians
        P1,P2,P3,P4 = [_min,_min],[_max,_min],[_max,_max],[_min,_max]
        P1,P2,P3,P4 = rotate(P1,center,f),rotate(P2,center,f), rotate(P3,center,f), rotate(P4,center,f)
        return Rectangle([P1,P2,P3,P4])
    elif shape == "Polygon":
        num = np.random.randint(3,100)	
        return Polygon(np.random.uniform(-1000, 1000, (num,2)))
    elif shape == "Circle":
        r = np.random.uniform(0.1,1000)
        [x, y] = np.random.uniform(-1000,1000, 2)
        return Circle(r,(x,y))
    elif shape =="Ellipse":
        [a, b] = np.random.uniform(0.1,1000, 2)
        [x, y] = np.random.uniform(-1000,1000, 2)
        f = 360*np.random.uniform(0,1)
        return Ellipse(a, b, f, (x, y))
    else:
        raise ValueError("Invalid shape type for creating random shape")

# Rotate P1 around P2 for angle f in radians        
# https://stackoverflow.com/questions/4465931/rotate-rectangle-around-a-point

def rotate(P1, P2, f):
    
    x = cos(f) * (P1[0]-P2[0]) - sin(f) * (P1[1]-P2[1]) + P2[0]
    y = sin(f) * (P1[0]-P2[0]) + cos(f) * (P1[1]-P2[1]) + P2[1]
    return [x,y]



# (https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/)

def intersect(A,B,C,D):
    def ccw(A,B,C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def parallel(A,B,C,D):
    if B[0] == A[0]: return (True if C[0] == D[0] else False)
    if C[0] == D[0]: return (True if A[0] == B[0] else False)
    return (B[1]-A[1])/(B[0]-A[0]) == (D[1]-C[1])/(D[0]-C[0])

# Taken and modified from 
# https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
# (bobobobo answer)


def Line_Intersect_Circle(A, B, C, r):
    d = (B[0]-A[0],B[1]-A[1])
    f = (A[0]-C[0],A[1]-C[1])

    a = d[0]*d[0]+d[1]*d[1]
    b = 2*(f[0]*d[0]+f[1]*d[1])
    c = f[0]*f[0]+f[1]*f[1]- r*r
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return False
    else:
        discriminant = sqrt(discriminant)
        t1 = (-b - discriminant)/(2*a)
        t2 = (-b + discriminant)/(2*a)
        if t1 >= 0 and t1 <= 1:
            return True
        if t2 >= 0 and t2 <= 1:
            return True
        return False
