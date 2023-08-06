# PyAllInOne (Jokes) - Init

''' This is the __init__.py file. '''

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
import json
import requests

# Function 1 - Get Joke
def get_joke(type="random"):
    # Checking the Data Type of "type"
    if (isinstance(type, str)):
        # Checking the Value of "type"
        if (type in ["random", "general", "programming", "knock-knock"]):
            # Fetching the Joke
            if (type == "random"):
                data = requests.get("https://official-joke-api.appspot.com/jokes/random")
            elif (type == "general"):
                data = requests.get("https://official-joke-api.appspot.com/jokes/general/random")
            elif (type == "programming"):
                data = requests.get("https://official-joke-api.appspot.com/jokes/programming/random")
            elif (type == "knock-knock"):
                data = requests.get("https://official-joke-api.appspot.com/jokes/knock-knock/random")

            # Converting the Data to a Dictionary
            jsonData = json.loads(data.text)

            # Converting List to Dictionary
            if (isinstance(jsonData, list)):
                jsonData = dict(jsonData[0])

            # Deleting the "type" and "id" Keys
            del jsonData["type"]
            del jsonData["id"]

            # Returning the Joke
            return jsonData
        else:
            raise Exception("The 'type' argument must be either 'random', 'general', 'programming', or 'knock-knock'.")
    else:
        raise TypeError("The 'type' argument must be a string.")