#!/usr/bin/env python


import argparse

import cv2
import time
import numpy as np

# Minimum area for detection
MIN_AREA = 50

DEF_WIDTH = 160
DEF_HEIGHT = 120

x_start, y_start, x_end, y_end = 0, 0, 0, 0
range_min = (0, 0, 0)
range_max = (0, 0, 0)
cropping = False
getROI = False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
        action="store_true", default=False,
        help="Increase output verbosity")
    parser.add_argument("-f", "--flip",
        action="store_true", default=False,
        help="Flip video to mirror the view")
    parser.add_argument("--width",
        default=DEF_WIDTH,
        help="Video width")
    parser.add_argument("--height",
        default=DEF_HEIGHT,
        help="Video height")
    return parser.parse_args()


def select_region(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, getROI
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        getROI = True


def main():
    global getROI, range_min, range_max

    args = parse_args()

    cv2.namedWindow("Input")
    cv2.namedWindow("HSV")
    cv2.namedWindow("Mask")
    cv2.namedWindow("Erosion")

    cv2.setMouseCallback("Input", select_region)

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    while True:
        grabbed, frame = capture.read()
        if not grabbed or frame is None:
            continue
        if args.flip:
            frame = np.fliplr(frame).copy()
        img_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(img_HSV, range_min, range_max)
        img_erode = cv2.erode(img_mask, None, iterations=3)
        moments = cv2.moments(img_erode, True)
        if moments['m00'] >= MIN_AREA:
            x = moments['m10'] / moments['m00']
            y = moments['m01'] / moments['m00']
            print(x, ", ", y)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)

        if cropping and not getROI:
            cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        elif not cropping and getROI:
            cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

        if getROI:
            roi = frame[y_start:y_end, x_start:x_end]
            hsvROI = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            print('min H = {}, min S = {}, min V = {}; max H = {}, max S = {}, max V = {}'.format(
                hsvROI[:,:,0].min(), hsvROI[:,:,1].min(), hsvROI[:,:,2].min(),
                hsvROI[:,:,0].max(), hsvROI[:,:,1].max(), hsvROI[:,    :,2].max()))
            range_min = np.array([hsvROI[:,:,0].min(), hsvROI[:,:,1].min(), hsvROI[:,:,2].min()])
            range_max = np.array([hsvROI[:,:,0].max(), hsvROI[:,:,1].max(), hsvROI[:,:,2].max()])
            getROI = False

        cv2.imshow("Input", frame)
        cv2.imshow("HSV", img_HSV)
        cv2.imshow("Mask", img_mask)
        cv2.imshow("Erosion", img_erode)

        key = cv2.waitKey(10)
        if key == ord('q'):
            # quit
            break
        elif key == ord('r'):
            # reset selection
            getROI = False


    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
