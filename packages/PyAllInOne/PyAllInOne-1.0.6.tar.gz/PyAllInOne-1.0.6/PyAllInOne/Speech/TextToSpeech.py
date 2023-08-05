# PyAllInOne (Speech) - TextToSpeech

''' This is the "TextToSpeech" module. '''

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
import pyttsx3

# Function 1 - Get Voices
def get_voices():
    # Creating the Engine
    engine = pyttsx3.init()

    # Getting the Voices
    voices = engine.getProperty("voices")

    # Stopping the Engine
    engine.stop()

    # Returning the Voices
    return voices

# Function 2 - Save
def save(data):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Keys
        keys = list(data.keys())

        # Checking for "text"
        if ("text" in keys and data["text"] != None and isinstance(data["text"], str)):
            # Checking for "voice"
            if ("voice" in keys and data["voice"] != None and isinstance(data["voice"], int)):
                # Checking for "rate"
                if ("rate" in keys and data["rate"] != None and isinstance(data["rate"], int)):
                    # Checking for "volume"
                    if ("volume" in keys and data["volume"] != None and isinstance(data["volume"], (int, float))):
                        # Checking for "path"
                        if ("path" in keys and data["path"] != None and isinstance(data["path"], str)):
                            # Creating the Engine
                            engine = pyttsx3.init()

                            # Setting the Properties
                            engine.setProperty("voice", engine.getProperty("voices")[data["voice"]].id)
                            engine.setProperty("rate", data["rate"])
                            engine.setProperty("volume", data["volume"])

                            # Saving the File
                            engine.save_to_file(data["text"], data["path"])
                            engine.runAndWait()
                        else:
                            raise Exception("The 'path' key must be present in the 'data' dictionary. It's value must be a string.")
                    else:
                        raise Exception("The 'volume' key must be present in the 'data' dictionary. It's value must be an integer or a float.")
                else:
                    raise Exception("The 'rate' key must be present in the 'data' dictionary. It's value must be an integer.")
            else:
                raise Exception("The 'voice' key must be present in the 'data' dictionary. It's value must be an integer.")
        else:
            raise Exception("The 'text' key must be present in the 'data' dictionary. It's value must be a string.")
    else:
        raise TypeError("The data must be in the form of a dictionary.")

# Function 3 - Say
def say(data):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Keys
        keys = list(data.keys())

        # Checking for "text"
        if ("text" in keys and data["text"] != None and isinstance(data["text"], str)):
            # Checking for "voice"
            if ("voice" in keys and data["voice"] != None and isinstance(data["voice"], int)):
                # Checking for "rate"
                if ("rate" in keys and data["rate"] != None and isinstance(data["rate"], int)):
                    # Checking for "volume"
                    if ("volume" in keys and data["volume"] != None and isinstance(data["volume"], (int, float))):
                        # Creating the Engine
                        engine = pyttsx3.init()

                        # Setting the Properties
                        engine.setProperty("voice", engine.getProperty("voices")[data["voice"]].id)
                        engine.setProperty("rate", data["rate"])
                        engine.setProperty("volume", data["volume"])

                        # Converting Text to Speech
                        engine.say(data["text"])
                        engine.runAndWait()
                    else:
                        raise Exception("The 'volume' key must be present in the 'data' dictionary. It's value must be an integer or a float.")
                else:
                    raise Exception("The 'rate' key must be present in the 'data' dictionary. It's value must be an integer.")
            else:
                raise Exception("The 'voice' key must be present in the 'data' dictionary. It's value must be an integer.")
        else:
            raise Exception("The 'text' key must be present in the 'data' dictionary. It's value must be a string.")
    else:
        raise TypeError("The data must be in the form of a dictionary.")