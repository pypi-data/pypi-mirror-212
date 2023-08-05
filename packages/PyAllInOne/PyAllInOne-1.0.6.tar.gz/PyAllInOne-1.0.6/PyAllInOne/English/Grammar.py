# PyAllInOne (English) - Grammar

''' This is the "Grammar" module. '''

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
from gingerit.gingerit import GingerIt

# Function 1 - Capitalized
def capitalized(phrase):
    # Checking the Data Type of "phrase"
    if (isinstance(phrase, str)):
        # Checking if Phrase is Capitalized
        if (phrase[0] >= "A" and phrase[0] <= "Z"):
            return True
        elif (phrase[0] >= "a" and phrase[0] <= "z"):
            return False
    else:
        raise TypeError("The 'phrase' argument must be a string.")

# Function 2 - Correct
def correct(text, full_result=False):
    # Checking the Data Type of "text"
    if (isinstance(text, str)):
        # Checking the Data Type of "full_result"
        if (isinstance(full_result, bool)):
            # Returning the Corrected Text
            if (full_result):
                return GingerIt().parse(text)
            else:
                return GingerIt().parse(text)["result"]
        else:
            raise TypeError("The 'full_result' argument must be a boolean.")
    else:
        raise TypeError("The 'text' argument must be a string.")