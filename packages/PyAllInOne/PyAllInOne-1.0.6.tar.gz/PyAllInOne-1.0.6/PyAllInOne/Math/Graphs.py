# PyAllInOne (Math) - Graphs

''' This is the "Graphs" module. '''

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
import matplotlib.pyplot as plt
import numpy as np

# Function 1 - Bar
def bar(data):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Keys
        keys = list(data.keys())

        # Checking for "x_values"
        if ("x_values" in keys and data["x_values"] != None and isinstance(data["x_values"], (list, tuple))):
            # Checking for "y_values"
            if ("y_values" in keys and data["y_values"] != None and isinstance(data["y_values"], (list, tuple))):
                # Checking for "x_label"
                if ("x_label" in keys and data["x_label"] != None and isinstance(data["x_label"], str)):
                    # Checking for "y_label"
                    if ("y_label" in keys and data["y_label"] != None and isinstance(data["y_label"], str)):
                        # Checking for "title"
                        if ("title" in keys and data["title"] != None and isinstance(data["title"], str)):
                            # Variables
                            command = 'plt.bar(data["x_values"], data["y_values"]'

                            # New "Data" Dictionary
                            newData = dict(data)
                            for key in ["x_values", "y_values", "x_label", "y_label", "title"]: del newData[key]
                            newKeys = list(newData.keys())

                            # Checking if "newKeys" is Empty
                            if (len(newKeys) != 0):
                                # Adding Extra Paramters
                                for key in newKeys:
                                    if (key == "font_size" or key == "grid"):
                                        pass
                                    elif (isinstance(data[key], (int, float))):
                                        command = command + ", " + key + "=" + str(data[key])
                                    elif (isinstance(data[key], str)):
                                        command = command + ", " + key + "=" + "'" + str(data[key]) + "'"

                                # Creating the Bar Chart
                                exec(command + ")")
                            else:
                                # Creating the Bar Chart
                                exec(command + ")")

                            # Checking for "font_size"
                            if ("font_size" in keys and data["font_size"] != None and isinstance(data["font_size"], (int, float))):
                                # Creating the Bar Chart
                                plt.xlabel(data["x_label"], fontsize=data["font_size"])
                                plt.ylabel(data["y_label"], fontsize=data["font_size"])
                                plt.title(data["title"], fontsize=data["font_size"])
                            else:
                                # Creating the Bar Chart
                                plt.xlabel(data["x_label"])
                                plt.ylabel(data["y_label"])
                                plt.title(data["title"])

                            # Checking for "grid"
                            if ("grid" in keys and data["grid"] != None and isinstance(data["grid"], bool)):
                                # Creating the Bar Chart
                                plt.grid(data["grid"])

                            # Showing the Bar Chart
                            plt.show()
                        else:
                            raise Exception("The 'title' key should be present in the 'data' dictionary. It's value should be a string.")
                    else:
                        raise Exception("The 'y_label' key should be present in the 'data' dictionary. It's value should be a string.")
                else:
                    raise Exception("The 'x_label' key should be present in the 'data' dictionary. It's value should be a string.")
            else:
                raise Exception("The 'y_values' key should be present in the 'data' dictionary. It's value should be a list or a tuple.")
        else:
            raise Exception("The 'x_values' key should be present in the 'data' dictionary. It's value should be a list or a tuple.")
    else:
        raise TypeError("The data must be in the form of a dictionary.")

# Function 2 - Line
def line(data):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Keys
        keys = list(data.keys())

        # Checking for "x_values"
        if ("x_values" in keys and data["x_values"] != None and isinstance(data["x_values"], (list, tuple))):
            # Checking for "y_values"
            if ("y_values" in keys and data["y_values"] != None and isinstance(data["y_values"], (list, tuple))):
                # Checking for "x_label"
                if ("x_label" in keys and data["x_label"] != None and isinstance(data["x_label"], str)):
                    # Checking for "y_label"
                    if ("y_label" in keys and data["y_label"] != None and isinstance(data["y_label"], str)):
                        # Checking for "title"
                        if ("title" in keys and data["title"] != None and isinstance(data["title"], str)):
                            # Variables
                            command = 'plt.plot(data["x_values"], data["y_values"]'

                            # New "Data" Dictionary
                            newData = dict(data)
                            for key in ["x_values", "y_values", "x_label", "y_label", "title"]: del newData[key]
                            newKeys = list(newData.keys())

                            # Checking if "newKeys" is Empty
                            if (len(newKeys) != 0):
                                # Adding Extra Paramters
                                for key in newKeys:
                                    if (key == "font_size" or key == "grid"):
                                        pass
                                    elif (key == "no_line" and isinstance(data[key], bool) and data[key] == True):
                                        command = command + ", 'o'"
                                    elif (key != "no_line" and isinstance(data[key], (int, float))):
                                        command = command + ", " + key + "=" + str(data[key])
                                    elif (key != "no_line" and isinstance(data[key], str)):
                                        command = command + ", " + key + "=" + "'" + str(data[key]) + "'"

                                # Creating the Line Chart
                                exec(command + ")")
                            else:
                                # Creating the Line Chart
                                exec(command + ")")

                            # Checking for "font_size"
                            if ("font_size" in keys and data["font_size"] != None and isinstance(data["font_size"], (int, float))):
                                # Creating the Line Chart
                                plt.xlabel(data["x_label"], fontsize=data["font_size"])
                                plt.ylabel(data["y_label"], fontsize=data["font_size"])
                                plt.title(data["title"], fontsize=data["font_size"])
                            else:
                                # Creating the Line Chart
                                plt.xlabel(data["x_label"])
                                plt.ylabel(data["y_label"])
                                plt.title(data["title"])

                            # Checking for "grid"
                            if ("grid" in keys and data["grid"] != None and isinstance(data["grid"], bool)):
                                # Creating the Line Chart
                                plt.grid(data["grid"])

                            # Showing the Line Chart
                            plt.show()
                        else:
                            raise Exception("The 'title' key should be present in the 'data' dictionary. It's value should be a string.")
                    else:
                        raise Exception("The 'y_label' key should be present in the 'data' dictionary. It's value should be a string.")
                else:
                    raise Exception("The 'x_label' key should be present in the 'data' dictionary. It's value should be a string.")
            else:
                raise Exception("The 'y_values' key should be present in the 'data' dictionary. It's value should be a list or a tuple.")
        else:
            raise Exception("The 'x_values' key should be present in the 'data' dictionary. It's value should be a list or a tuple.")
    else:
        raise TypeError("The data must be in the form of a dictionary.")

# Function 3 - Pie
def pie(data):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Keys
        keys = list(data.keys())

        # Checking for "values"
        if ("values" in keys and data["values"] != None and isinstance(data["values"], (list, tuple))):
            # Variables
            command = 'plt.pie(np.array(data["values"])'

            # New "Data" Dictionary
            newData = dict(data)
            for key in ["values"]: del newData[key]
            newKeys = list(newData.keys())

            # Checking if "newKeys" is Empty
            if (len(newKeys) != 0):
                # Adding Extra Paramters
                for key in newKeys:
                    if (key == "legend" or key == "legend_title"):
                        pass
                    elif (isinstance(data[key], (int, float, list, tuple))):
                        command = command + ", " + key + "=" + str(data[key])
                    elif (isinstance(data[key], str)):
                        command = command + ", " + key + "=" + "'" + str(data[key]) + "'"

                # Creating the Pie Chart
                exec(command + ")")
            else:
                # Creating the Pie Chart
                exec(command + ")")

            # Checking for "legend"
            if ("legend" in keys and data["legend"] != None and isinstance(data["legend"], bool) and data["legend"] == True):
                if ("legend_title" in keys and data["legend_title"] != None and isinstance(data["legend_title"], str)):
                    # Creating the Pie Chart
                    plt.legend(title = data["legend_title"])
                else:
                    # Creating the Pie Chart
                    plt.legend()

            # Showing the Pie Chart
            plt.show()
        else:
            raise Exception("The 'values' key should be present in the 'data' dictionary. It's value should be a list or a tuple.")
    else:
        raise TypeError("The data must be in the form of a dictionary.")