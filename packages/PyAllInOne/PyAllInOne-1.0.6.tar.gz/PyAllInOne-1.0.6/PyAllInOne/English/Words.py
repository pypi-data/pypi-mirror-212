# PyAllInOne (English) - Words

''' This is the "Words" module. '''

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
import os
import json
from difflib import get_close_matches

# The Directory
directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

# Function 1 - Meaning
def meaning(word):
    # Variables
    dictionaryJSON = json.load(open(directory + "/assets/dictionary.json", encoding="utf8"))

    # Checking the Data Type of "word"
    if (isinstance(word, str)):
        # Converting to Lower Case
        word = word.lower()

        # Checking for the Meaning
        if (word in dictionaryJSON):
            # Returning the Meaning
            return dictionaryJSON[word]
        elif (len(get_close_matches(word, dictionaryJSON.keys())) > 0):
            return "Did you mean '{0}' instead? Try it again with the correct word.".format(get_close_matches(word, dictionaryJSON.keys())[0])
        else:
            return "The word doesn't exist. Please try again."
    else:
        raise TypeError("The 'word' argument must be a string.")

# Function 2 - Anagram
def anagram(phrase1, phrase2):
    # Checking the Data Type of "phrase1" and "phrase2"
    if (isinstance(phrase1, str) and isinstance(phrase2, str)):
        # Converting to Lower Case
        phrase1 = phrase1.lower()
        phrase2 = phrase2.lower()

        # Checking if Anagram
        return ((len(phrase1) == len(phrase2)) and (sorted(phrase1) == sorted(phrase2)))
    else:
        raise TypeError("The 'phrase1' and 'phrase2' arguments must be a string.")