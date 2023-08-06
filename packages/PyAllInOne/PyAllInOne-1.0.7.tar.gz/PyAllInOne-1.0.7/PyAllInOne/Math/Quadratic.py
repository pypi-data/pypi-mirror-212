# PyAllInOne (Math) - Quadratic

''' This is the "Quadratic" module. '''

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

# Function 1 - Find Discriminant
def find_discriminant(a, b, c):
    newA = float(a)
    newB = float(b)
    newC = float(c)

    # Returning the Discriminant
    return (b**2) - (4*a*c)

# Function 2 - Find Roots
def find_roots(a, b, c):
    newA = float(a)
    newB = float(b)
    newC = float(c)

    discriminant = findDiscriminant(a, b, c)

    alpha = (-newB + math.sqrt(discriminant)) / (2*newA)
    beta = (-newB - math.sqrt(discriminant)) / (2*newA)

    # Returning the Roots
    return (alpha, beta)