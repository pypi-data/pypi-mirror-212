# PyAllInOne (Files) - Init

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
import os
import mimetypes

# Function 1 - Exists
def exists(path):
    return os.path.exists(path)

# Function 2 - File Type
def file_type(path):
    # Initializing Mimetypes
    mimetypes.init()

    # Checking if Path Exists
    if (exists(path)):
        # Returning the File Type
        return mimetypes.guess_type(path)[0].split("/")[0]
    else:
        raise FileNotFoundError("The file path doesn't exist.")