# PyAllInOne (Traffic) - People Detection

''' This is the "PeopleDetection" module. '''

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
import imutils
import mimetypes

# The Directory
directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

# Sample Media
SampleVideo1 = directory + "/assets/sample_media/PeopleDetection/videos/1.mp4"
SampleVideo2 = directory + "/assets/sample_media/PeopleDetection/videos/2.mp4"
SampleVideo3 = directory + "/assets/sample_media/PeopleDetection/videos/3.mp4"
SampleVideo4 = directory + "/assets/sample_media/PeopleDetection/videos/4.mp4"
SampleVideo5 = directory + "/assets/sample_media/PeopleDetection/videos/5.mp4"

# Initializing the HOG Descriptor
detector = cv2.HOGDescriptor()
detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Function 1 - Detect
def detect(frame, function):
    # Setting the Box Coordinates & Styles
    bounding_box_cordinates, weights =  detector.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)

    # Detecting the People
    person = 1

    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f"Person {person}", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

        person += 1

        # Performing the User Function
        if ((function is not None) and (callable(function))):
            function()

    # Placing Text on the Output
    cv2.putText(frame, f"Total People: {person-1}", (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

    # Showing the Output
    cv2.imshow("People Detection", frame)
    return frame

# Function 2 - Detect By Video
def detect_by_video(path, function):
    # Initializing the Video
    video = cv2.VideoCapture(path)
    check, frame = video.read()

    # Checking if the Video is Null
    if (check == False):
        raise Exception("There's something wrong with the video. Try again with another one.")

    # Opening the Video and Sending Video Data to the "detect()" Function
    while video.isOpened():
        check, frame = video.read()

        if (check):
            frame = imutils.resize(frame, width=min(800, frame.shape[1]))
            frame = detect(frame, function)

            # Clicking "q" Closes the Video
            if (cv2.waitKey(1) == ord("q")):
                break
        else:
            raise Exception("There's something wrong with the video. Try again with another one.")
            break

    # Stopping OpenCV
    video.release()
    cv2.destroyAllWindows()

# Function 3 - Detect People
def detect_people(path, show=False, function=None):
    # Checking if Path Exists
    if (os.path.exists(path)):
        # Checking the File Type
        mimetypes.init()
        fileType = mimetypes.guess_type(path)[0].split("/")[0]

        if (fileType == "image"): # Image
            # Reading the Image
            image = cv2.imread(path)

            # Detecting the Humans
            (humans, _) = detector.detectMultiScale(image, winStride=(10, 10), padding=(32, 32), scale=1.1)

            for (x, y, w, h) in humans:
                pad_w, pad_h = int(0.15 * w), int(0.01 * h)
                cv2.rectangle(image, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)

                # Performing the User Function
                if ((function is not None) and (callable(function))):
                    function()

            # Returning the Image
            if (show):
                cv2.imshow("People Detection", image)
                cv2.waitKey(0)

            # Returning the Count
            return len(humans)
        elif (fileType == "video"): # Video
            # Sending the Video to the "detect_by_video()" Function
            detect_by_video(path, function)
        else:
            raise Exception("The file provided must be an image or a video.")
    else:
        raise FileNotFoundError("The file path doesn't exist.")