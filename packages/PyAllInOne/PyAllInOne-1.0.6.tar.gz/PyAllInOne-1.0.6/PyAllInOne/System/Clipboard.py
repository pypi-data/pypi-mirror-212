# PyAllInOne (System) - Clipboard

''' This is the "Clipboard" module. '''

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
import pyperclip

# Function 1 - Copy
def copy(text):
    # Checking the Data Type of "text"
    if (isinstance(text, str)):
        # Copying the Text
        pyperclip.copy(text)
    else:
        raise TypeError("The 'text' argument must be a string.")

# Function 2 - Paste
def paste():
    return pyperclip.paste()