#!/usr/bin/env python


import argparse

import cv2
import time
import numpy as np

BLUE = 'blue'
GREEN = 'green'
RED = 'red'
ORANGE = 'orange'

BGR = 'bgr'
HSV = 'hsv'
HSV_MIN = 'hsv_min'
HSV_MAX = 'hsv_max'

COLOUR_MAP = {
    BLUE : {
        HSV_MIN : (110, 50, 50),
        HSV_MAX : (130, 255, 255),
        BGR : (255, 0, 0),
    },
    GREEN : {
        HSV_MIN : (42, 62, 63),
        HSV_MAX : (92, 255, 235),
        BGR : (0, 255, 0),
    },
    RED : {
        HSV_MIN : (0, 131, 126),
        HSV_MAX : (179, 255, 255),
        BGR : (0, 0, 255),
    },
    ORANGE : {
        HSV_MIN : (0, 150, 210),
        HSV_MAX : (44, 291, 286),
        BGR : (0, 165, 255),
    }
}

# Minimum area for detection
MIN_AREA = 50

DEF_WIDTH = 160
DEF_HEIGHT = 120


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
        action="store_true", default=False,
        help="increase output verbosity")
    parser.add_argument("--width",
        default=DEF_WIDTH,
        help="Video width")
    parser.add_argument("--height",
        default=DEF_HEIGHT,
        help="Video height")
    parser.add_argument("-c", "--colour",
        default=GREEN,
        help="The colour to track")
    return parser.parse_args()


def main():
    args = parse_args()

    colour = args.colour
    range_min = COLOUR_MAP[colour][HSV_MIN]
    range_max = COLOUR_MAP[colour][HSV_MAX]
    dot_colour = COLOUR_MAP[colour][BGR]

    cv2.namedWindow("Input")
    cv2.namedWindow("HSV")
    cv2.namedWindow("Mask")
    cv2.namedWindow("Erosion")

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    while True:
        grabbed, frame = capture.read()
        if not grabbed or frame is None:
            continue
        img_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(img_HSV, range_min, range_max)
        img_erode = cv2.erode(img_mask, None, iterations=3)
        moments = cv2.moments(img_erode, True)
        if moments['m00'] >= MIN_AREA:
            x = moments['m10'] / moments['m00']
            y = moments['m01'] / moments['m00']
            print(x, ", ", y)
            cv2.circle(frame, (int(x), int(y)), 5, dot_colour, -1)

        cv2.imshow("Input",frame)
        cv2.imshow("HSV", img_HSV)
        cv2.imshow("Mask", img_mask)
        cv2.imshow("Erosion", img_erode)

        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
