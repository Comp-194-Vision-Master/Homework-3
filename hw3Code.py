"""
File: hw3Code.py

This file contains the functions for Homework 3, along with some sample tests.

Fall 2025
Author: Susan Fox
"""

# TODO: Add your name as author of this code file


import random
import cv2
import numpy as np


# ----------------------------------------------------------------------------------------------------------------
# Question 1


# TODO: Put your definition of bubbleMix here


# ----------------------------------------------------------------------------------------------------------------
# Question 2


# TODO: Replace each of the TODO comments below by a comment that describes either
# TODO: the function or the lines that follow. More details are in the instructions


def getBox(pic):
    # TODO: Put a triple-quoted docstring here that describes overall what getBox does
    boxSz = 100
    canvSz = 6 * boxSz
    smPic = cv2.resize(pic, (boxSz, boxSz))
    (baseCanvas, targLoc) = initCanvas(boxSz, canvSz)

    # TODO: Add a hash-mark comment here that explains what shiftX and shiftY are for
    shiftX = 0
    shiftY = 0
    while True:
        # TODO: Add a hash-mark comment here that describes  what the next 4 lines do
        shiftX2 = shiftX + boxSz
        shiftY2 = shiftY + boxSz
        trMat = np.float32([[1, 0, shiftX], [0, 1, shiftY]])
        shiftedIm = cv2.warpAffine(smPic, trMat, (canvSz, canvSz))

        # TODO: Add a hash-mark comment here that describes what the next 4 lines do
        maskShift = 255 - np.zeros(shiftedIm.shape, shiftedIm.dtype)
        cv2.rectangle(maskShift, (shiftX, shiftY), (shiftX2, shiftY2), (0, 0, 0), -1)
        maskCanvas = cv2.bitwise_and(baseCanvas, maskShift)
        viewCanvas = shiftedIm + maskCanvas

        cv2.imshow("Canvas", viewCanvas)

        # TODO: Add a hash-mark comment here that describes what the if statement is for
        if onTarget((shiftX, shiftY, shiftX2, shiftY2), targLoc):
            won = True
            break
        else:
            # TODO: Add a hash-mark comment here that describes what this section does
            x = cv2.waitKey()
            if x > 0:
                ch = chr(x)
                if ch == 'q':
                    won = False
                    break
                elif ch == 'w':
                    shiftY -= 10
                elif ch == 'a':
                    shiftX -= 10
                elif ch == 's':
                    shiftY += 10
                elif ch == 'd':
                    shiftX += 10

        # TODO: Add a hash-mark comment here that describes what the next three lines do
        if moveTarget():
            counter = 0
            baseCanvas, targLoc = initCanvas(boxSz, canvSz)

    # TODO: Add a hash-mark comment that explains the purpose of the next line
    showFinal(viewCanvas, won)


def initCanvas(boxSize, canvasSize):
    # TODO: Add a triple-quoted docstring here that describes the purpose of this function
    canv = np.zeros((canvasSize, canvasSize, 3), np.uint8)
    targSize = boxSize + 10
    targX = random.randint(0, canvasSize - targSize)
    targY = random.randint(0, canvasSize - targSize)
    cv2.rectangle(canv, (targX, targY), (targX + targSize, targY + targSize), (0, 180, 0), -1)
    return canv, (targX, targY, targX + targSize, targY + targSize)


def onTarget(playerLoc, targetLoc):
    # TODO: Add a triple-quoted docstring here that describes the purpose of this function
    (tx1, ty1, tx2, ty2) = targetLoc
    (px1, py1, px2, py2) = playerLoc
    return (tx1 <= px1) and (px2 <= tx2) and (ty1 <= py1) and (py2 <= ty2)


def moveTarget():
    # TODO: Add a triple-quoted docstring here that describes the purpose of this function
    n = random.random()
    return n <= 0.10


def showFinal(canvas, didWin):
    # TODO: Add a triple-quoted docstring here that describes the purpose of this function
    lastCanv = canvas.copy()
    lastCanv = cv2.add(lastCanv, 60)
    (cHgt, cWid, cDep) = canvas.shape
    x = cWid // 4
    y = cHgt // 2
    if didWin:
        cv2.putText(lastCanv, "You win!!", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    else:
        cv2.putText(lastCanv, "You lose!!", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    cv2.imshow("Canvas", lastCanv)
    cv2.waitKey()


# ----------------------------------------------------------------------------------------------------------------
# Question 3


# TODO: Implement adjustHue, adjustSat, and adjustVal using the pseudocode in the assignment

def findBall(img):
    """Takes in an image, and displays it, allowing the user to adjust settings for the hue, saturation,
    and value boundaries used by inRange. Ultimately, when the user finishes the final image with a contour
    and a circle draw on on it, along with the final bounds, and the center point and radius of the circle, are
    returned."""
    currHue = 60
    lowBounds = (currHue - 10, 0, 0)
    highBounds = (currHue + 10, 255, 255)
    while True:
        lowBounds, highBounds, center, radius = adjustHue(img, lowBounds, highBounds)
        lowBounds, highBounds, center, radius = adjustSat(img, lowBounds, highBounds)
        lowBounds, highBounds, center, radius = adjustVal(img, lowBounds, highBounds)

        finalResult, center, radius = applyBounds(img, lowBounds, highBounds, "Space to continue, q to quit")
        cv2.imshow("Ball Finder", finalResult)
        x = cv2.waitKey()
        if chr(x) == 'q':
            break
    return finalResult, lowBounds, highBounds, center, radius


def applyBounds(imag, low, high, taskStr):
    """Takes in an image, the low and high bounds, and a descriptive string to write on the image. It uses
    inRange on the HSV version of the image to find colors that fit within the bounds. It finds the largest
    contour formed by the threshold image, and draws it and the smallest enclosing circle around it. Returns
    the modified image (with contour and circle drawn on it), as well as the center position of the circle,
    and its radius."""
    hsvImg = cv2.cvtColor(imag, cv2.COLOR_BGR2HSV)
    imgCopy = imag.copy()
    thresh = cv2.inRange(hsvImg, low, high)
    contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return imgCopy
    biggest = contours[0]
    bigArea = cv2.contourArea(biggest)
    for cont in contours:
        currArea = cv2.contourArea(cont)
        if currArea > bigArea:
            biggest = cont
            bigArea = currArea

    cv2.drawContours(imgCopy, [biggest], -1, (255, 255, 0), 2)
    circ = cv2.minEnclosingCircle(biggest)
    center, fRad = circ
    cx = int(center[0])
    cy = int(center[1])
    crad = int(fRad)
    cv2.circle(imgCopy, (cx, cy), crad, (0, 0, 255), 2)
    cv2.putText(imgCopy, taskStr, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    cv2.putText(imgCopy, str(low), (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    cv2.putText(imgCopy, str(high), (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    return imgCopy, (cx, cy), crad

# TODO: Put your definitions of adjustHue, adjustSat, and adjustVal below here


# ----------------------------------------------------------------------------------------------------------------
# Question 4

# TODO: Write your pseudocode for this question in the triple-quoted string below


"""
Algorithm morphVideo(source)


"""


# ----------------------------------------------------------------------------------------------------------------
# Question 5


# TODO: Modify the camshift2 function below to track two objects (of different colors)

def camshift2(refImage1):
    """Takes in a reference image and sets up the Camshift process for it. It makes a histograms, and sets
    up two a track window. It then runs Camshift on the images from a videe feed, using the histogram and
    track window, and draws the resulting track box as an ellipse on the image."""
    cam = cv2.VideoCapture(0)
    hueHist1 = makeHueHist(refImage1)
    trackWindow1 = None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("No more frames...")
            break

        frame = cv2.flip(frame, 1)
        hgt, wid, dep = frame.shape

        # Initialize the track window to be the whole frame the first time
        if emptyTrackWindow(trackWindow1):
            trackWindow1 = (0, 0, wid, hgt)

        trackBox1, trackWindow1 = processFrame(frame, trackWindow1, hueHist1)
        cv2.ellipse(frame, trackBox1, (0, 0, 255), 2)

        cv2.imshow('camshift', frame)
        v = cv2.waitKey(5)
        if v > 0 and chr(v) == 'q':
            break


def makeHueHist(refImage):
    """Takes in a reference image, and it builds a histogram of its hue values. It masks away low value or
    low saturation pixels, leaving them out of the histogram. It normalizes the values in the histogram so that
    the max value is 255, letting us map from histogram values directly to brightness values in the back projection.
    It returns the histogram it created."""
    hsvRef = cv2.cvtColor(refImage, cv2.COLOR_BGR2HSV)
    maskedHistIm = cv2.inRange(hsvRef, (0, 60, 32), (180, 255, 255))
    hist = cv2.calcHist([hsvRef], [0], maskedHistIm, [16], [0, 180])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    hist = hist.reshape(-1)
    show_hist(hist)
    return hist


def emptyTrackWindow(trackW):
    """Takes in the current track window. If the track window is None, then this is the first frame, so we return
    True: the track wondow is empty right now and should be reset. If the track window exists, but its size is too
    small, then it returns True: the track window is nearly empty and should be reset. Otherwise, it returns False,
    meaning that the track window is not empty."""
    if trackW is None:
        return True
    else:
        (x1, y1, x2, y2) = trackW
        return abs(x2 - x1) < 5 or abs(y2 - y1) < 5


def processFrame(image, trackWindow, hist):
    """Takes in an image, the track window and the histogram, and it runs the Camshift process. It converts
    the image to HSV, masks away low saturation and low value pixels, and calculates the back-projection for
    the resulting image. It then runs Camshift, which updates the position of the track window and creates a
    track box, a rotated rectangle, for the object being tracked. It returns the track box and the track window."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # convert to HSV
    maskHSV = cv2.inRange(hsv, (0, 60, 32), (180, 255, 255))
    prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    prob &= maskHSV
    cv2.imshow("Backproject", prob)

    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    trackBox, trackWindow = cv2.CamShift(prob, trackWindow, term_crit)
    return trackBox, trackWindow


def show_hist(hist):
    """Takes in the histogram, and displays it in the histogram window."""
    bin_count = hist.shape[0]
    bin_w = 24
    image = np.zeros((256, bin_count * bin_w, 3), np.uint8)
    for i in range(bin_count):
        h = int(hist[i])
        cv2.rectangle(image,
                      (i * bin_w + 2, 255),
                      ((i + 1) * bin_w - 2, 255 - h),
                      (int(180.0 * i / bin_count), 255, 255),
                      -1)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imshow('histogram', image)


# ----------------------------------------------------------------------------------------------------------------
# Question 6

# TODO: Put a triple-quote string below this and in it write what your goals are for
# TODO: this question: what "vibe", tone, or feeling did you want to create, and how
# TODO: do your choices of transformations achieve that

# TODO: Write your videoVibe program here as defined in the instructions


# ----------------------------------------------------------------------------------------------------------------
# Main script

# TODO: Uncomment the sample calls below to start testing your code (add calls if you like)

if __name__ == "__main__":
    print("Sample calls...")
    # -------------------------------------------------------------
    # Question 1 sample calls
    # print("Testing question 1:  bubbleMix")
    # img1 = cv2.imread("SampleImages/winterRobin.jpg")
    # img2 = cv2.imread("SampleImages/selbyWinter.jpg")
    # img3 = cv2.imread("SampleImages/raspberries.jpg")
    # img4 = cv2.imread("SampleImages/bearLake.jpg")
    #
    # finalPic1 = bubbleMix(img2, img1)
    # cv2.imshow("BubbleMix", finalPic1)
    # cv2.imwrite("BubbleExample.png", finalPic1)
    # cv2.waitKey()
    #
    # finalPic2 = bubbleMix(img4, img3)
    # cv2.imshow("BubbleMix", finalPic2)
    # cv2.waitKey()

    # -------------------------------------------------------------
    # Question 2 sample calls
    # print("Testing question 2:  getBox")
    #
    # pic = cv2.imread("SampleImages/catSitting.jpg")
    # getBox(pic)

    # -------------------------------------------------------------
    # Question 3 sample calls
    # print("Testing question 3:  findBall")
    #
    # pic1 = cv2.imread("SampleImages/BallFinding/Blue1BG1Mid.jpg")
    # pic2 = cv2.imread("SampleImages/BallFinding/YellowBG1Mid.jpg")
    # img, lb, ub, cent, rads = findBall(pic1)
    # print("blue:", lb, ub, cent, rads)
    # img2, lb, ub, cent, rads = findBall(pic2)
    # print("yellow:", lb, ub, cent, rads)

    # -------------------------------------------------------------
    # Question 5 sample calls
    # print("Testing question 4:  camshift2")
    # blueRef = cv2.imread("SampleImages/refPics/refBlue.png")
    # pinkRef = cv2.imread("SampleImages/refPics/refPink.jpg")
    # greenRef = cv2.imread("SampleImages/refPics/refGreen.png")
    # camshift2(blueRef, greenRef)

    # -------------------------------------------------------------
    # Question 6 sample calls
    # print("Testing question 6:  videoVibe")
    # videoVibe(0)
