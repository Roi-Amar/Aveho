"""
Aveho (by Roi) was built to give a greenscreen with no greenscreen to the masses
feel free to share and make use of the code below
"""

import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
"""set the capture from the webcam (numbers may differ, if you cant see your camera try to change the number to 
another one. """
cap2 = cv2.VideoCapture("gs_.mp4")  # green screen video
# subtract = cv2.createBackgroundSubtractorMOG2(history=40, varThreshold=60, detectShadows=False) # use of motion detection - off by default
# subtract = cv2.createBackgroundSubtractorKNN(history=1, detectShadows=False) # use of motion detection - off by default
"""empty function for the use of the track bars"""


def nothing(_):
    pass


"""this part takes an empty photo of the background for late comparison"""
_, origin = cap.read()
time.sleep(1)
_, origin = cap.read()  # capture again because of camera delay
_, gs = cap2.read()
originGray = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)  # convert to gray to deduct "noise"
originGray = cv2.GaussianBlur(originGray, (9, 9), 0)  # cast blur to deduct "noise"

"""this part is for the control panels (here you can change the default values)"""
panel = np.zeros([100, 700], np.uint8)
cv2.namedWindow("panel") # this is the diffrence panel (shadow mask)
cv2.createTrackbar("threshold L", "panel", 25, 255, nothing)
cv2.createTrackbar("kernel vertical", "panel", 2, 70, nothing)
cv2.createTrackbar("kernel horizontal", "panel", 2, 70, nothing)
cv2.createTrackbar("kernel vertical2", "panel", 2, 70, nothing)
cv2.createTrackbar("kernel horizontal2", "panel", 2, 70, nothing)
cv2.createTrackbar("maskK v", "panel", 2, 70, nothing)
cv2.createTrackbar("maskK h", "panel", 2, 70, nothing)

panel2 = np.zeros([100, 700], np.uint8)
cv2.namedWindow("panel2")  # this is the color panel (color mask)
cv2.createTrackbar("L - h", "panel2", 0, 179, nothing)
cv2.createTrackbar("H - h", "panel2", 45, 179, nothing)
cv2.createTrackbar("L - s", "panel2", 110, 255, nothing)
cv2.createTrackbar("H - s", "panel2", 205, 255, nothing)
cv2.createTrackbar("L - v", "panel2", 50, 255, nothing)
cv2.createTrackbar("H - v", "panel2", 255, 255, nothing)

panel3 = np.zeros([100, 700], np.uint8)
cv2.namedWindow("panel3")  # this is the shadow edges panel
cv2.createTrackbar("kerE h", "panel3", 16, 100, nothing)
cv2.createTrackbar("kerE v", "panel3", 16, 100, nothing)
cv2.createTrackbar("kerD h", "panel3", 3, 70, nothing)
cv2.createTrackbar("kerD v", "panel3", 3, 70, nothing)
cv2.createTrackbar("Ditr", "panel3", 2, 20, nothing)

while True:
    """this part is the mask panel connection"""
    t_l = cv2.getTrackbarPos("threshold L", "panel")
    dial_v = cv2.getTrackbarPos("kernel vertical", "panel")
    dial_h = cv2.getTrackbarPos("kernel horizontal", "panel")
    dial_v2 = cv2.getTrackbarPos("kernel vertical2", "panel")
    dial_h2 = cv2.getTrackbarPos("kernel horizontal2", "panel")
    dial_mv = cv2.getTrackbarPos("maskK v", "panel")
    dial_mh = cv2.getTrackbarPos("maskK h", "panel")

    """this part is the mask panel2 connection"""
    l_h = cv2.getTrackbarPos("L - h", "panel2")
    h_h = cv2.getTrackbarPos("H - h", "panel2")
    l_s = cv2.getTrackbarPos("L - s", "panel2")
    h_s = cv2.getTrackbarPos("H - s", "panel2")
    l_v = cv2.getTrackbarPos("L - v", "panel2")
    h_v = cv2.getTrackbarPos("H - v", "panel2")

    """this part is the mask panel3 connection"""
    e_h = cv2.getTrackbarPos("kerE h", "panel3")
    e_v = cv2.getTrackbarPos("kerE v", "panel3")
    d_h = cv2.getTrackbarPos("kerD h", "panel3")
    d_v = cv2.getTrackbarPos("kerD v", "panel3")
    ditr = cv2.getTrackbarPos("Ditr", "panel3")

    """kernel for morph"""
    kernel = np.ones((dial_v, dial_h), np.uint8)
    kernel2 = np.ones((dial_v2, dial_h2), np.uint8)
    kernelM = np.ones((dial_mv, dial_mh), np.uint8)
    kernelE = np.ones((e_h, e_v), np.uint8)
    kernelD = np.ones((d_h, d_v), np.uint8)

    """set frame grab"""
    _, frame = cap.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to gray to deduct "noise"
    frameGray = cv2.GaussianBlur(frameGray, (9, 9), 0)  # cast blur to deduct "noise"
    # sub = subtract.apply(frameGray) # use of motion detection

    """set color mask"""
    colorHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to hsv
    lowerRange = np.array([l_h, l_s, l_v])  # create lower range
    upperRange = np.array([h_h, h_s, h_v])  # create upper range
    colorMask = cv2.inRange(colorHsv, lowerRange, upperRange)
    colorMask = cv2.bilateralFilter(colorMask, 9, 75, 75)  # use filters to deduct "noise"
    colorMask = cv2.GaussianBlur(colorMask, (5, 5), 0)
    colorMask = cv2.morphologyEx(colorMask, cv2.MORPH_CLOSE, kernel2)
    _, colorMask = cv2.threshold(colorMask, 30, 255, cv2.THRESH_BINARY)  # color again in black and white

    """set color edge mask"""
    edgesC = cv2.Canny(colorMask, 100, 100)
    edgesC = cv2.morphologyEx(edgesC, cv2.MORPH_CLOSE, kernelE)
    edgesC = cv2.dilate(edgesC, kernel=np.ones((2, 2), np.uint8), iterations=2)
    edgesC = cv2.GaussianBlur(edgesC, (5, 5), 0)

    """find a change between background photo and camera feed"""
    diff = cv2.absdiff(originGray, frameGray)
    _, diffThr = cv2.threshold(diff, t_l, 255, cv2.THRESH_BINARY)  # set threshold to deduct "noise"
    shadow_mask = cv2.morphologyEx(diffThr, cv2.MORPH_CLOSE, kernel)
    shadow_mask = cv2.GaussianBlur(shadow_mask, (5, 5), 0)

    """set shadow edges mask"""
    edges = cv2.Canny(diffThr, 100, 100)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernelE)
    edges = cv2.dilate(edges, kernel=kernelD, iterations=ditr)
    edges = cv2.GaussianBlur(edges, (5, 5), 0)

    """combine the color and shadow masks"""
    mask = cv2.bitwise_or(shadow_mask, cv2.morphologyEx(colorMask, cv2.MORPH_CLOSE, kernelM))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelM)
    mask = cv2.bitwise_or(mask, edges)
    mask = cv2.bitwise_or(mask, edgesC)
    _, mask = cv2.threshold(mask, 30, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    fg = cv2.bitwise_and(frame, frame, mask=mask)  # foreground is the frame without the mask
    bg = cv2.bitwise_and(gs, gs, mask=mask_inv)  # background is the greenscreen without the inv_mask
    unified = cv2.bitwise_xor(fg, bg)

    """this part show the feed windows to the screen"""
    cv2.imshow("unified", unified)
    cv2.imshow("panel", panel)  #
    cv2.imshow("panel2", panel2)
    cv2.imshow("panel3", panel3)

    """delete the '#' mark in order to see the screen"""
    # cv2.imshow("fg", fg) # show only the foreground
    # cv2.imshow("bg", bg) # show only the background
    cv2.imshow("mask", mask)  # show only the mask
    cv2.imshow("colorMask", colorMask)  # show only the mask
    cv2.imshow("shadow_mask", shadow_mask)  # show only the mask
    cv2.imshow("edges", edges)  # show only the mask
    cv2.imshow("edgesC", edgesC)  # show only the mask

    """press Esc to exit"""
    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
