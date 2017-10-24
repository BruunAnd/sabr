import abc
import cv2
import numpy as np
from Interfaces import ITargetInfo
from ImageFeed import ImageFeedWebcamera

class TargetInfo(ITargetInfo):

    _camera = None
    _sample_size = None

    def __init__(self, capture_device = 0, sample_size = 10):
        self._camera = cv2.VideoCapture(capture_device)
        self._sample_size = sample_size

    def image_processing(self):
        sample_data = self.get_sample_data()

        frame_width = np.shape(sample_data[0])[1]

        bounding_boxes = []

        # For help on colorspaces: https://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html
        lower_hsv_colour = np.array([169,100,100])
        upper_hsv_colour = np.array([189,255,255])

        for frame in sample_data:
            # Convert the current frame to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Create a mask of the image (everything within the threshold appears white and everything else is black)
            mask = cv2.inRange(hsv, lower_hsv_colour, upper_hsv_colour)

            # Get rid of background noise using erosion
            element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
            mask = cv2.erode(mask, element, iterations=2)
            mask = cv2.dilate(mask, element, iterations=2)
            mask = cv2.erode(mask, element)

            # Create Contours for all objects in the defined colorspace
            _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) == 0:
                continue

            # Search through the Countours for the largest object
            best_contour = max(contours, key = cv2.contourArea)

            # Create a bounding box around the largest object
            if best_contour is not None:
                bounding_boxes.append(cv2.boundingRect(best_contour))

        # Return the coordinate sets
        return (bounding_boxes, frame_width)

    def get_sample_data(self):
        sample_data = []

        for i in range(0, self._sample_size):
            ret, frame = self._camera.read() 
            sample_data.append(frame)
        
        return sample_data