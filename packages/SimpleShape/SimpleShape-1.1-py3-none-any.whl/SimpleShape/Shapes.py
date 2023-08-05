"""
Main document with classes and methods
"""

import json
from math import pi, sqrt, sin, cos
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse as _Ellipse
import numpy as np
import warnings


class Geometry:
    """Parent class for creating geometric objects"""
    
    def __init__(self, coordinates):
        """Initialization of the object. Somewhat different for
        circle and ellipse"""
        self.coordinates = coordinates
    
    def __str__(self) -> str:
        """A string representation of the object"""
        return ("The coordinates of the " + self.__class__.__name__ + " are " + 
        str(self.coordinates))

    def perimeter(self) -> float:
        """Perimeter (circumference) of object"""
        s = 0
        for i in range(len(self.coordinates)):
            s += sqrt((self.coordinates[i-1][0] - self.coordinates[i][0])**2 +
                      (self.coordinates[i-1][1] - self.coordinates[i][1])**2)
        return s
    
    def area(self) -> float:
        """Area of object using Shoelace formula"""
        s = 0
        for i in range(len(self.coordinates)):             
            s += (self.coordinates[i-1][0] * self.coordinates[i][1] -
                  self.coordinates[i][1] * self.coordinates[i-1][1])
        return abs(s/2)

    def to_json(self) -> json:
        """Convert the object to .json format"""
        if self.__class__.__name__ in ('Triangle', 'Rectangle', 'Polygon'):
            return {
                'type': self.__class__.__name__,
                'coordinates': self.coordinates
            }
        elif self.__class__.__name__ == 'Circle':
            return {
                'type': self.__class__.__name__,
                'r': self.r,
                'center':self.center
            }
        elif self.__class__.__name__ == 'Ellipse':
            return {
                'type': self.__class__.__name__,
                'a': self.a,
                'b': self.b,
                'f': self.f,
                'center':self.center
            }
        else:
            raise Warning('Invalid JSON data. Try something else')

    def from_json(cls, json_data) -> object:
        """Create a geometric object from JSON data."""
        
        if json_data['type'] in ('Triangle', 'Rectangle', 'Polygon'):
            return Rectangle(json_data['coordinates'])
        elif json_data['type'] == 'Circle':
            return Circle(json_data['r'], json_data['center'])
        elif json_data['type'] == 'Ellipse':
            return Ellipse(json_data['a'],json_data['b'],
                           json_data['f'], json_data['center'])
        else:
            raise Warning('Invalid JSON data. Try something else')
            
    def save_shapes(shapes, filename):
        """Save json_data to file"""
        json_data = [element.to_json() for element in shapes]
        with open(filename, 'w') as file:
            json.dump(json_data, file)

    def load_shapes(filename):
        """Load json_data from file"""
        with open(filename, 'r') as file:
            json_data = json.load(file)
            shapes = [Geometry.from_json(data) for data in json_data]
            return shapes 
            
    
    def intersect(self, other) -> bool:
        if self.__class__.__name__ in ('Triangle','Rectangle','Polygon'):
            if isinstance(other, (Triangle or Rectangle or Polygon)):
                for i in range(-1,len(self.coordinates)-1):
                    for j in range(-1,len(other.coordinates)-1):
                        if intersect(self.coordinates[i-1],self.coordinates[i],
                                     other.coordinates[j-1],other.coordinates[j]):
                            return True
                return False
            elif isinstance(other, Circle):
                for i in range(-1,len(self.coordinates)-1):
                    if Line_Intersect_Circle(other.center, other.r, self.p1, self.p2):
                        return True
                return False
            
            elif isinstance(other, Ellipse):
                return "This feature has yet to be implemented"
            else:
                raise ValueError("Invalid shape type for intersection check")
            
        
       
        elif self.__class__.__name__ == ('Circle'):
            if isinstance(other, Circle):
                return sqrt((self.center[0]-other.center[0])**2+
                            (self.center[1]-other.center[1])**2) < (self.r+other.r)
            elif isinstance(other, (Triangle or Rectangle or Polygon)):
                for i in range(-1,len(other.coordinates)-1):
                    if Line_Intersect_Circle(self.center, self.r, other.p1, other.p2):
                        return True
                return False
            elif isinstance(other, Ellipse):
                return "This feature has yet to be implemented"
            else:
                raise ValueError("Invalid shape type for intersection check")

    
        elif self.__class__.__name__ == ('Ellipse'):
            return "This feature has yet to be implemented"
        else:
            raise ValueError("Invalid shape type for intersection check")
            
    
    def visualize(self) -> None:
        
        X = np.array(self.coordinates)
        plt.figure()
        plt.scatter(X[:, 0], X[:, 1], s = 20)
        t1 = plt.Polygon(X[:3,:])
        plt.gca().add_patch(t1)
        
        pass


# Basic shapes (rectangle, Triangle, circle, elipsoid, point, line)

class Triangle(Geometry):
    
    def __init__(self, coordinates):
        super().__init__(coordinates)

        self.a = coordinates[0][:2]
        self.b = coordinates[1][:2]
        self.c = coordinates[2][:2]
        
        if (2 > len(self.a) or 2 > len(self.b) or 2 > len(self.c)):
            return warnings.warn("Provide a 3x2 array or tuple")
        
        if parallel(self.a,self.b,self.b,self.c):
            return warnings.warn("Not a triangle. Try again")

    
    
class Rectangle(Geometry):
    """Coordinates inserted as 4x2 tuple or array in the following order:
        lower left, lower right, upper right, upper left"""
        
    def __init__(self, coordinates):
        super().__init__(coordinates)
        self.a = coordinates[0][:2]
        self.b = coordinates[1][:2]
        self.c = coordinates[2][:2]
        self.d = coordinates[3][:2]
        
        if (2 > len(self.a) or 2 > len(self.b) or 2 > len(self.c) or 2 > len(self.d)):
            raise Exception("Provide a 4x2 array or tuple")
        if not (parallel(self.a,self.b,self.c,self.d) and parallel(self.b,self.c,self.a,self.d)):
            raise Warning('Not a rectangle. Try something else')
            
class Polygon(Geometry):
    """Three or more-dimensional geometric shape. Insert coordinates in
    specific order"""
    def __init__(self, coordinates):
        super().__init__(coordinates)


class Circle(Geometry):
    
    def __init__(self, r, center = (0,0)):
        self.r = r
        self.center = center
        
        if r <= 0: return warnings.warn("Radius is less than equal than 0. Use another radius")
    
    def __str__(self):
        return ("Circle with radius " + str(self.r) + " and center in " +
                str(self.center)) 

    def area(self):
        return pi * self.r**2

    def perimeter(self):
        return 2 * pi * self.r
           
           
    def visualize(self):
        circle=plt.Circle(self.center, self.r, color='r')
        fig, ax = plt.subplots()
        ax.set_xlim(((self.center[0]-self.r)*1.1, (self.center[0]+self.r)*1.1))
        ax.set_ylim(((self.center[1]-self.r)*1.1, (self.center[1]+self.r)*1.1))
        ax.add_patch(circle)
        
    
class Ellipse(Geometry):
    def __init__(self, a, b, f = 0, center = (0,0)):
        self.a = a
        self.b = b
        self.f = f
        self.center = center
        
    def __str__(self):
        return ("Ellipse with a = " + str(self.a) + ", b = " + str(self.b) +
                ", rotation of " + str(self.f) + " and center at " +str(self.center)) 

    def area(self):
        return pi * self.a * self.b

    def perimeter(self):
        """Approximate calculation using Ramaujan formula"""
        return pi * (3*(self.a+self.b) - 
                     sqrt( (3*self.a + self.b) * (self.a + 3*self.b) ) )
           
    def visualize(self):
        fig, ax = plt.subplots()

        ax.axis('equal')
        ell = _Ellipse(xy=self.center, width=self.a, height=self.b, angle=self.f
                       , lw=4, facecolor='b')
        
        ax.add_artist(ell)
        
        temp = max(self.a,self.b)
        ax.set_xlim(((self.center[0]-temp)*1.1, (self.center[0]+temp)*1.1))
        ax.set_ylim(((self.center[1]-temp)*1.1, (self.center[1]+temp)*1.1))
        
        plt.show()



        
def random_shape(shape = next(iter({"Rectangle", "Triangle", "Circle", "Ellipse", "Polygon"}))):
    
    if shape =="Triangle":
        return Triangle(np.random.uniform(-1000, 1000, (3,2)))
    elif shape =="Rectangle":
        [a, b] = np.random.uniform(-1000,1000, (2,1))
        _min = min(a,b)[0]
        _max = max(a,b)[0]
        f = 2*pi*np.random.uniform(0,1) # Radians
        P1,P2,P3,P4 = [_min,_min],[_max,_min],[_max,_max],[_min,_max]
        P2,P3,P4 = rotate(P2,P1,f), rotate(P3,P1,f), rotate(P4,P1,f)
        return Rectangle([P1,P2,P3,P4])
    elif shape =="Polygon":
        num = np.random.randint(3,100)	
        cord = []
        """for i in range(num):
            while 1<2:
                a,b = np.random.uniform(-1000, 1000)
                check intersect
                if not intersect:
                    cord.append([a,b])
                    continue"""
         
        return Polygon(cord)
    elif shape =="Circle":
        r = np.random.uniform(0,1000)
        [x, y] = np.random.uniform(-1000,1000, (2,1))
        return Circle(r,(x,y))
    elif shape =="Ellipse":
        [a, b] = np.random.uniform(0,1000, (2,1))
        [x, y] = np.random.uniform(-1000,1000, (2,1))
        f = 360*np.random.uniform(0,1)
        return Ellipse(a, b, f, (x,y))
    else:
        raise ValueError("Invalid shape type for creating random shape")

# Rotate P1 around P2 for angle f in radians        
# https://stackoverflow.com/questions/4465931/rotate-rectangle-around-a-point

def rotate(P1, P2, f):
    
    x = cos(f) * (P2[0]-P1[0]) - sin(f) * (P2[1]-P1[1]) + P1[0]
    y = sin(f) * (P2[0]-P1[0]) + cos(f) * (P2[1]-P1[1]) + P1[1]
    return [x,y]



# (https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/)

def intersect(A,B,C,D):
    def ccw():
        return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def parallel(A,B,C,D):
    if B[0] == A[0]: return (True if C[0] == D[0] else False)
    return abs((B[1]-A[1])/(B[0]-A[0])) == abs((D[1]-C[1])/(D[0]-C[0]))

# Taken and modified from 
# https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
# (chmike answer)

def Line_Intersect_Circle(A, B, c, r):

    LAB = sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
    
    Dx = (B[0]-A[0])/LAB
    Dy = (B[1]-A[1])/LAB
    
    t = Dx * (c[0] - A[0]) + Dy * (c[1] - A[1])    
    
    Ex = t*Dx+A[0]
    Ey = t*Dy+A[1]
    
    LEC = sqrt((Ex-c[0])**2+(Ey-c[0])**2)
    
    if LEC <= r: return True

    return False
    
