# PyAllInOne (Math) - Trigonometry

''' This is the "Trigonometry" module. '''

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

# Functions - Conversions
def degrees_to_radians(degrees): return degrees * (3.14/180)
def radians_to_degrees(radians): return radians * (180/3.14)

# Functions - Trigonometric Ratios
def sin(radians): return math.sin(radians)
def cos(radians): return math.cos(radians)
def tan(radians): return math.tan(radians)
def cosec(radians): return 1 / (sin(radians))
def sec(radians): return 1 / (cos(radians))
def cot(radians): return 1 / (tan(radians))