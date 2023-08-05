# PyAllInOne (Traffic) - Vehicle Detection

''' This is the "VehicleDetection" module. '''

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
import cv2
import time
import mimetypes
import numpy as np
from PIL import Image

# The Directory
directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

# OpenCV Cascade Classifier (Car)
car_cascade = cv2.CascadeClassifier(directory + "/assets/models/haarcascade_car.xml")

# Sample Media
SampleImage1 = directory + "/assets/sample_media/VehicleDetection/images/1.jpg"
SampleImage2 = directory + "/assets/sample_media/VehicleDetection/images/2.jpg"
SampleImage3 = directory + "/assets/sample_media/VehicleDetection/images/3.jpg"
SampleImage4 = directory + "/assets/sample_media/VehicleDetection/images/4.jpg"
SampleImage5 = directory + "/assets/sample_media/VehicleDetection/images/5.jpg"
SampleImage6 = directory + "/assets/sample_media/VehicleDetection/images/6.jpg"
SampleImage7 = directory + "/assets/sample_media/VehicleDetection/images/7.jpg"
SampleImage8 = directory + "/assets/sample_media/VehicleDetection/images/8.jpg"
SampleImage9 = directory + "/assets/sample_media/VehicleDetection/images/9.jpg"
SampleImage10 = directory + "/assets/sample_media/VehicleDetection/images/10.jpg"

SampleVideo1 = directory + "/assets/sample_media/VehicleDetection/videos/1.mp4"

# Function 1 - Detect Cars
def detect_cars(path, show=False):
    # Checking if Path Exists
    if (os.path.exists(path)):
        # Checking the File Type
        mimetypes.init()
        fileType = mimetypes.guess_type(path)[0].split("/")[0]

        if (fileType == "image"): # Image
            # Opening the Image
            image = Image.open(path)
            image = image.resize((450, 250))
            image_arr = np.array(image)

            # Converting Image to Greyscale
            grey = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
            Image.fromarray(grey)

            # Blurring the Image
            blur = cv2.GaussianBlur(grey, (5,5), 0)
            Image.fromarray(blur)

            # Dilating the Image
            dilated = cv2.dilate(blur, np.ones((3,3)))
            Image.fromarray(dilated)

            # Morphology
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
            Image.fromarray(closing)

            # Identifying the Cars
            cars = car_cascade.detectMultiScale(closing, 1.1, 1)

            # Counting the Cars
            count = 0

            for (x, y, w, h) in cars:
                cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
                count += 1

            # Returning the Image
            if (show):
                cv2.imshow("Vehicle Detection - Cars", image_arr)
                cv2.waitKey(0)

            # Returning the Count
            return count
        elif (fileType == "video"): # Video
            # Opening the Video
            video = cv2.VideoCapture(path)

            # Opening the Video and Processing
            while video.isOpened():
                time.sleep(.05)

                # Reading the First Frame
                ret, frame = video.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Identifying the Cars
                cars = car_cascade.detectMultiScale(gray, 1.4, 2)

                for (x,y,w,h) in cars:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.imshow("Vehicle Detection - Cars", frame)

                # Clicking "q" Closes the Video
                if cv2.waitKey(1) == ord("q"):
                    break

            # Stopping OpenCV
            video.release()
            cv2.destroyAllWindows()
        else:
            raise Exception("The file provided must be an image or a video.")
    else:
        raise FileNotFoundError("The file path doesn't exist.")