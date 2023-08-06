# PyAllInOne (Math) - Geometry

''' This is the "Geometry" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import math

# Constants
pi = 3.14159
goldenRatio = 1.61803

# Function 1 - Area (Areas and Volumes)
def area(**kwargs):
    shapeList = ["square", "rectangle", "triangle", "circle", "parallelogram", "trapezium", "rhombus"]
    keyList = []

    for key, value in kwargs.items():
        keyList.append(key)

    if ("shape" in keyList):
        if (kwargs["shape"] in shapeList):
            shape = kwargs["shape"]

            if (shape == "square"): # Square
                if ("side" in keyList):
                    if (isinstance(kwargs["side"], (int, float))):
                        return kwargs["side"] * kwargs["side"]
                    else:
                        raise TypeError("The 'side' argument must be an integer or a float.")
                else:
                    raise Exception("To check the area of a square, the 'side' argument must be present.")
            elif (shape == "rectangle"): # Rectangle
                if ("length" in keyList and "width" in keyList):
                    if (isinstance(kwargs["length"], (int, float)) and isinstance(kwargs["width"], (int, float))):
                        return kwargs["length"] * kwargs["width"]
                    else:
                        raise TypeError("The 'length' and 'width' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the area of a rectangle, the 'length' and 'width' arguments must be present.")
            elif (shape == "triangle"): # Triangle
                if ("base" in keyList and "height" in keyList):
                    if (isinstance(kwargs["base"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return 0.5 * kwargs["base"] * kwargs["height"]
                    else:
                        raise TypeError("The 'base' and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the area of a triangle, the 'base' and 'height' arguments must be present.")
            elif (shape == "circle"): # Circle
                if ("radius" in keyList):
                    if (isinstance(kwargs["radius"], (int, float))):
                        return 3.14 * math.pow(kwargs["radius"], 2)
                    else:
                        raise TypeError("The 'radius' argument must be an integer or a float.")
                else:
                    raise Exception("To check the area of a circle, the 'radius' argument must be present.")
            elif (shape == "parallelogram"): # Parallelogram
                if ("base" in keyList and "height" in keyList):
                    if (isinstance(kwargs["base"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return kwargs["base"] * kwargs["height"]
                    else:
                        raise TypeError("The 'base' and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the area of a parallelogram, the 'base' and 'height' arguments must be present.")
            elif (shape == "trapezium"): # Trapezium
                if ("base1" in keyList and "base2" in keyList and "height" in keyList):
                    if (isinstance(kwargs["base1"], (int, float)) and isinstance(kwargs["base2"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return 0.5 * kwargs["height"] * (kwargs["base1"] + kwargs["base2"])
                    else:
                        raise TypeError("The 'base1', 'base2', and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the area of a trapezium, the 'base1', 'base2', and 'height' arguments must be present.")
            elif (shape == "rhombus"): # Rhombus
                if ("diagonal1" in keyList and "diagonal2" in keyList):
                    if (isinstance(kwargs["diagonal1"], (int, float)) and isinstance(kwargs["diagonal2"], (int, float))):
                        return (kwargs["diagonal1"] * kwargs["diagonal2"]) / 2
                    else:
                        raise TypeError("The 'diagonal' and 'diagonal2' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the area of a rhombus, the 'diagonal1' and 'diagonal2' arguments must be present.")
        else:
            raise Exception("The 'shape' argument must be a square, rectangle, triangle, circle, parallelogram, trapezium, or rhombus.")
    else:
        raise Exception("The 'shape' argument must be present in this function.")

# Function 2 - Volume (Areas and Volumes)
def volume(**kwargs):
    shapeList = ["cube", "cuboid", "cone", "cylinder", "sphere", "hemisphere", "pyramid"]
    keyList = []

    for key, value in kwargs.items():
        keyList.append(key)

    if ("shape" in keyList):
        if (kwargs["shape"] in shapeList):
            shape = kwargs["shape"]

            if (shape == "cube"): # Cube
                if ("side" in keyList):
                    if (isinstance(kwargs["side"], (int, float))):
                        return math.pow(kwargs["side"], 3)
                    else:
                        raise TypeError("The 'side' argument must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a cube, the 'side' argument must be present.")
            elif (shape == "cuboid"): # Cuboid
                if ("length" in keyList and "width" in keyList and "height" in keyList):
                    if (isinstance(kwargs["length"], (int, float)) and isinstance(kwargs["width"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return kwargs["length"] * kwargs["width"] * kwargs["height"]
                    else:
                        raise TypeError("The 'length', 'width', and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a cuboid, the 'length', 'width', and 'height' arguments must be present.")
            elif (shape == "cone"): # Cone
                if ("raidus" in keyList and "height" in keyList):
                    if (isinstance(kwargs["radius"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return (1/3) * 3.14 * math.pow(kwargs["radius"], 2) * kwargs["height"]
                    else:
                        raise TypeError("The 'radius' and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a cone, the 'radius' and 'height' arguments must be present.")
            elif (shape == "cylinder"): # Cylinder
                if ("radius" in keyList and "height" in keyList):
                    if (isinstance(kwargs["radius"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return 3.14 * math.pow(kwargs["radius"], 2) * kwargs["height"]
                    else:
                        raise TypeError("The 'radius' and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a cylinder, the 'radius' and 'height' arguments must be present.")
            elif (shape == "sphere"): # Sphere
                if ("radius" in keyList):
                    if (isinstance(kwargs["radius"], (int, float))):
                        return (4/3) * 3.14 * math.pow(kwargs["radius"], 3)
                    else:
                        raise TypeError("The 'radius' argument must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a sphere, the 'radius' argument must be present.")
            elif (shape == "hemisphere"): # Hemisphere
                if ("radius" in keyList):
                    if (isinstance(kwargs["radius"], (int, float))):
                        return (2/3) * 3.14 * math.pow(kwargs["radius"], 3)
                    else:
                        raise TypeError("The 'radius' argument must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a hemisphere, the 'radius' argument must be present.")
            elif (shape == "pyramid"): # Pyramid
                if ("length" in keyList and "width" in keyList and "height" in keyList):
                    if (isinstance(kwargs["length"], (int, float)) and isinstance(kwargs["width"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        return (length * width * height) / 3
                    else:
                        raise TypeError("The 'length', 'width', and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the volume of a pyramid, the 'length', 'width', and 'height' arguments must be present.")
        else:
            raise Exception("The 'shape' argument must be a cube, cuboid, cone, cylinder, sphere, hemisphere, or pyramid.")
    else:
        raise Exception("The 'shape' argument must be present in this function.")

# Function 3 - Surface Area (Areas and Volumes)
def surface_area(**kwargs):
    shapeList = ["cube", "cuboid", "cone", "cylinder", "sphere", "hemisphere"]
    keyList = []

    for key, value in kwargs.items():
        keyList.append(key)

    if ("shape" in keyList):
        if (kwargs["shape"] in shapeList):
            shape = kwargs["shape"]

            if (shape == "cube"): # Cube
                if ("side" in keyList):
                    if (isinstance(kwargs["side"], (int, float))):
                        if ("lateral" in keyList):
                            if (isinstance(kwargs["lateral"], bool)):
                                if (kwargs["lateral"] == True):
                                    return 4 * math.pow(side, 2)
                                else:
                                    return 6 * math.pow(side, 2)
                            else:
                                raise TypeError("The 'lateral' argument must be either True or False.")
                        else:
                            return 6 * math.pow(kwargs["side"], 2)
                    else:
                        raise TypeError("The 'side' argument must be an integer or a float.")
                else:
                    raise Exception("To check the surface area of a cube, the 'side' argument must be present.")
            elif (shape == "cuboid"): # Cuboid
                if ("length" in keyList and "width" in keyList and "height" in keyList):
                    if (isinstance(kwargs["length"], (int, float)) and isinstance(kwargs["width"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        if ("lateral" in keyList):
                            if (isinstance(kwargs["lateral"], bool)):
                                if (kwargs["lateral"] == True):
                                    return 2 * kwargs["height"] * (kwargs["length"] + kwargs["width"])
                                else:
                                    return 2 * ((kwargs["length"] * kwargs["width"]) + (kwargs["width"] * kwargs["height"]) + (kwargs["length"] * kwargs["height"]))
                            else:
                                raise TypeError("The 'lateral' argument must be either True or False.")
                        else:
                            return 2 * ((kwargs["length"] * kwargs["width"]) + (kwargs["width"] * kwargs["height"]) + (kwargs["length"] * kwargs["height"]))
                    else:
                        raise TypeError("The 'length', 'width', and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the surface area of a cuboid, the 'length', 'width', and 'height' arguments must be present.")
            elif (shape == "cone"): # Cone
                if ("raidus" in keyList and "height" in keyList):
                    if (isinstance(kwargs["radius"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        slantHeight = math.sqrt(math.pow(kwargs["radius"], 2) + math.pow(kwargs["height"], 2))

                        if ("lateral" in keyList):
                            if (isinstance(kwargs["lateral"], bool)):
                                if (kwargs["lateral"] == True):
                                    return 3.14 * kwargs["radius"] * slantHeight
                                else:
                                    return 3.14 * kwargs["radius"] * (slantHeight + kwargs["radius"])
                            else:
                                raise TypeError("The 'lateral' argument must be either True or False.")
                        else:
                            return 3.14 * kwargs["radius"] * (slantHeight + kwargs["radius"])
                    else:
                        raise TypeError("The 'radius' and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the surface area of a cone, the 'radius' and 'height' arguments must be present.")
            elif (shape == "cylinder"): # Cylinder
                if ("radius" in keyList and "height" in keyList):
                    if (isinstance(kwargs["radius"], (int, float)) and isinstance(kwargs["height"], (int, float))):
                        if ("lateral" in keyList):
                            if (isinstance(kwargs["lateral"], bool)):
                                if (kwargs["lateral"] == True):
                                    return 2 * 3.14 * kwargs["radius"] * kwargs["height"]
                                else:
                                    return 2 * 3.14 * kwargs["radius"] * (kwargs["radius"] + kwargs["height"])
                            else:
                                raise TypeError("The 'lateral' argument must be either True or False.")
                        else:
                            return 2 * 3.14 * kwargs["radius"] * (kwargs["radius"] + kwargs["height"])
                    else:
                        raise TypeError("The 'radius' and 'height' arguments must be an integer or a float.")
                else:
                    raise Exception("To check the surface area of a cylinder, the 'radius' and 'height' arguments must be present.")
            elif (shape == "sphere"): # Sphere
                if ("radius" in keyList):
                    if (isinstance(kwargs["radius"], (int, float))):
                        if ("lateral" in keyList):
                            if (isinstance(kwargs["lateral"], bool)):
                                if (kwargs["lateral"] == True):
                                    return 4 * 3.14 * math.pow(kwargs["radius"], 2)
                                else:
                                    return 4 * 3.14 * math.pow(kwargs["radius"], 2)
                            else:
                                raise TypeError("The 'lateral' argument must be either True or False.")
                        else:
                            return 4 * 3.14 * math.pow(kwargs["radius"], 2)
                    else:
                        raise TypeError("The 'radius' argument must be an integer or a float.")
                else:
                    raise Exception("To check the surface area of a sphere, the 'radius' argument must be present.")
            elif (shape == "hemisphere"): # Hemisphere
                if ("radius" in keyList):
                    if (isinstance(kwargs["radius"], (int, float))):
                        if ("lateral" in keyList):
                            if (isinstance(kwargs["lateral"], bool)):
                                if (kwargs["lateral"] == True):
                                    return 2 * 3.14 * math.pow(kwargs["radius"], 2)
                                else:
                                    return 3 * 3.14 * math.pow(kwargs["radius"], 2)
                            else:
                                raise TypeError("The 'lateral' argument must be either True or False.")
                        else:
                            return 3 * 3.14 * math.pow(kwargs["radius"], 2)
                    else:
                        raise TypeError("The 'radius' argument must be an integer or a float.")
                else:
                    raise Exception("To check the surface area of a hemisphere, the 'radius' argument must be present.")
        else:
            raise Exception("The 'shape' argument must be a cube, cuboid, cone, cylinder, sphere, or hemisphere.")
    else:
        raise Exception("The 'shape' argument must be present in this function.")

# Function 4 - Distance (Coordinate Geometry)
def distance(point1, point2):
    # Checking the Data Type of "point1" and "point2"
    if (isinstance(point1, tuple) and  isinstance(point2, tuple)):
        # Checking the Length of "point1" and "point2"
        if (len(point1) == 2 and len(point2) == 2 or len(point1) == 3 and len(point2) == 3):
            x1, x2 = point1[0], point2[0]
            y1, y2 = point1[1], point2[1]

            # Calculating the Distance
            if (len(point1) == 2 and len(point2) == 2): # 2D
                # Returning the Distance
                return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
            else: # 3D
                z1, z2 = point1[2], point2[2]

                # Returning the Distance
                return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2))
        else:
            raise Exception("Both points (tuples) must be in the form of (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂).")
    else:
        raise TypeError("The 'point1' and 'point2' arguments must be a tuple.")

# Function 5 - Is Collinear (Coordinate Geometry)
def is_collinear(point1, point2, point3):
    # Checking the Data Type of "point1", "point2", and "point3"
    if (isinstance(point1, tuple) and isinstance(point2, tuple) and isinstance(point3, tuple)):
        # Checking the Length of "point1", "point2", and "point3"
        if (len(point1) == 2 and len(point2) == 2 and len(point3) == 2 or len(point1) == 3 and len(point2) == 3 and len(point3) == 3):
            # Returning if Collinear
            return (distance(point1, point3) == distance(point1, point2) + distance(point2, point3))
        else:
            raise Exception("The 3 points (tuples) must be in the form of (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂).")
    else:
        raise TypeError("The 'point1', 'point2', and 'point3' arguments must be a tuple.")

# Function 6 - Section (Coordinate Geometry)
def section(point1, point2, ratio, typeOfSection="Internal"):
    # Checking the Data Type of "point1" and "point2"
    if (isinstance(point1, tuples) and isinstance(point2, tuple)):
        # Checking the Data Type of "ratio"
        if (isinstance(ratio, tuple)):
            # Checking the Type of "typeOfSection"
            if (typeOfSection in ["Internal", "External"]):
                # Checking the Length of "point1" and "point2"
                if (len(point1) == 2 and len(point2) == 2 or len(point1) == 3 and len(point2) == 3):
                    x1, x2 = point1[0], point2[0]
                    y1, y2 = point1[1], point2[1]
                    m, n = ratio[0], ratio[1]

                    # Checking the Section
                    if (len(point1) == 2 and len(point2) == 2): # 2D
                        if (typeOfSection == "Internal"):
                            # Returning the Section
                            return (((m * x2) + (n * x1)) / (m + n), ((m * y2) + (n * y1)) / (m + n))
                        elif (typeOfSection == "External"):
                            # Returning the Section
                            return (((m * x2) - (n * x1)) / (m - n), ((m * y2) - (n * y1)) / (m - n))
                    else: # 3D
                        z1, z2 = point1[2], point2[2]

                        if (typeOfSection == "Internal"):
                            # Returning the Section
                            return (((m * x2) + (n * x1)) / (m + n), ((m * y2) + (n * y1)) / (m + n), ((m * z2) + (n * z1)) / (m + n))
                        elif (typeOfSection == "External"):
                            # Returning the Section
                            return (((m * x2) - (n * x1)) / (m - n), ((m * y2) - (n * y1)) / (m - n), ((m * z2) - (n * z1)) / (m - n))
                else:
                    raise Exception("Both points (tuples) must be in the form of (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂).")
            else:
                raise Exception("The 'typeOfSection' argument must be either 'Internal' or 'External'.")
        else:
            raise TypeError("The 'ratio' argument must be a tuple in the form (m, n).")
    else:
        raise TypeError("The 'point1' and 'point2' arguments must be a tuple.")

# Functions - Circles
def circumference(radius): return 2 * 3.14 * radius
def diameter(radius): return 2 * radius
def area_of_sector(angle, radius): return (angle / 360) * 3.14 * math.pow(radius, 2)
def arc_length(angle, radius): return (angle / 360) * circumference(radius)

# Functions - Triangles
def hypotenuse(side1, side2): return math.sqrt(math.pow(side1, 2) + math.pow(side2, 2))
def herons_formula(side1, side2, side3):
    semiPerimeter = (side1 + side2 + side3) / 2

    # Returning the Area
    return math.sqrt(semiPerimeter * (semiPerimeter - side1) * (semiPerimeter - side2) * (semiPerimeter - side3))