# PyAllInOne (System) - Brightneszs

''' This is the "Brightness" module. '''

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
import screen_brightness_control as sbc
import platform

# Function 1 - Max
def max():
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Setting the Brightness
        sbc.set_brightness(100)
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 2 - Min
def min():
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Setting the Brightness
        sbc.set_brightness(0)
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 3 - Set
def set(value, display=0):
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Checking the Data Type of "value"
        if (isinstance(value, (int, float))):
            # Checking the Data Type of "display"
            if (isinstance(display, int)):
                # Setting the Brightness
                sbc.set_brightness(value, display=display)
            else:
                raise TypeError("The 'display' argument must be an integer.")
        else:
            raise TypeError("The 'value' argument must be an integer or a float.")
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 4 - Get
def get(display=0):
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Checking the Data Type of "display"
        if (isinstance(display, int)):
            # Returning the Data
            return {"Brightness": sbc.get_brightness(display=0), "Monitors": sbc.list_monitors()}
        else:
            raise TypeError("The 'display' argument must be an integer.")
    else:
        raise Exception("This function only works on Windows and Linux.")