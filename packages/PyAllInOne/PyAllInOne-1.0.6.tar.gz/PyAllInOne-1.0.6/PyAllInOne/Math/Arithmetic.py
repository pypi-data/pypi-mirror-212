# PyAllInOne (Math) - Arithmetic

''' This is the "Arithmetic" module. '''

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
import cmath

# Constants
iota = "Iota is also referred to as 'i'. It's value is √-1."

# Functions - Simple Arithmetic Operations
def add(num1, num2): return num1 + num2
def subtract(num1, num2): return num1 - num2
def multiply(num1, num2): return num1 * num2
def divide(num1, num2): return num1 / num2
def modulus(num1, num2): return num1 % num2
def floor_division(num1, num2): return num1 // num2
def power(base, exponent): return base ** exponent

# Functions - Complex Numbers
def modulus_complex(z): return abs(z)
def conjugate_complex(z): return z.conjugate()
def multiplicative_inverse_complex(z): return conjugateComplex(z) / power(modulusComplex(z), 2)
def polar_complex(z): return cmath.polar(z)

# Functions - Squares and Cubes
def square(number): return power(number, 2)
def cube(number): return power(number, 3)
def square_root(number): return number ** 0.5
def cube_root(number): return number ** (1/3)

# Functions - Odd and Even
def is_odd(number): return number % 2 == 1
def is_even(number): return number % 2 == 0

# Function 1 - Factorial
def factorial(number):
    # Checking the Data Type of "number"
    if (isinstance(number, int)):
        f = 1

        for i in range(1, number + 1):
            f = f * i

        # Returning the Factorial
        return f
    else:
        raise TypeError("The 'terms' argument must be an integer.")

# Function 2 - Fibonacci
def fibonacci(terms):
    # Checking the Data Type of "terms"
    if (isinstance(terms, int)):
        if (terms == 0):
            return None
        elif (terms == 1):
            return [0]
        elif (terms == 2):
            return [0, 1]
        else:
            f = 0
            s = 1

            list = [f, s]

            for i in range(2, terms):
                t = f + s

                list.append(t)

                f = s
                s = t

            # Returning the Fibonacci Series
            return list
    else:
        raise TypeError("The 'terms' argument must be an integer.")

# Function 3 - HCF
def hcf(num1, num2):
    # Checking the Data Type of "num1" and "num2"
    if (isinstance(num1, int) and isinstance(num2, int)):
        hcf = 1

        for i in range(1, min(num1, num2)):
            if num1 % i == 0 and num2 % i == 0:
                hcf = i

        # Returning the HCF
        return hcf
    else:
        raise TypeError("The 'num1' and 'num2' arguments must be an integer.")

# Function 4 - LCM
def lcm(num1, num2):
    # Checking the Data Type of "num1" and "num2"
    if (isinstance(num1, int) and isinstance(num2, int)):
        if (num1 > num2):
            greater = num1
        else:
            greater = num2

        while True:
            if ((greater % num1 == 0) and (greater % num2 == 0)):
                lcm = greater
                break

            greater += 1

        # Returning the LCM
        return lcm
    else:
        raise TypeError("The 'num1' and 'num2' arguments must be an integer.")

# Function 5 - Prime
def is_prime(number):
    # Checking the Data Type of "number"
    if (isinstance(number, int)):
        isPrime = False

        if (number < 1):
            isPrime = False
        else:
            for i in range(2, int(number/2) + 1):
                if (number % i == 0):
                    isPrime = False
                    break
            else:
                isPrime = True

        # Checking if Prime
        return isPrime
    else:
        raise TypeError("The 'number' argument must be an integer.")