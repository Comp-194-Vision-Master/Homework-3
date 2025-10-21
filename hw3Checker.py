"""
File: hw3Checker.py

This file contains test functions that check solutions for Homework 3, using assert to check if the results are fine
or indicating to the user that they should visually check the work.

Fall 2025
Author: Susan Fox
"""

# TODO: Change  hw3CodeSoln below to match your solution filename

import hw3CodeSoln as hw3
import cv2


# ==========================================================================================
# Testing main program

# Comment in our out the calls to the checker functions in runTests below. You don't need to change anything
# else in this file


def runTests():
    """Calls testing functions"""
    print("Running tests...")

    # Question 1
    # check_bubbleMix()

    # Question 3
    # check_findBall()

    # Question 4
    # check_camshift2()

    # Question 5
    # check_videoVibe()


# ----------------------------------------------------------------------------------------------------------------
# Question 1


def check_bubbleMix():
    """Tests bubbleMix to see if it works"""
    print("Testing bubbleMix...")

    im1 = cv2.imread("SampleImages/selbyWinter.jpg")
    im2 = cv2.imread("SampleImages/winterRobin.jpg")
    im3 = cv2.imread("SampleImages/bearLake.jpg")
    im4 = cv2.imread("SampleImages/raspberries.jpg")

    new1 = hw3.bubbleMix(im1, im2)
    new2 = hw3.bubbleMix(im3, im4)
    new3 = hw3.bubbleMix(im2, im1)
    new4 = hw3.bubbleMix(im2, im4)
    cv2.imshow("Bubble Mix 1", new1)
    cv2.imshow("Bubble Mix 2", new2)
    cv2.imshow("Bubble Mix 3", new3)
    cv2.imshow("Bubble Mix 4", new4)
    cv2.waitKey()
    print("-------------Must Check Visually By Hand!-------------")


# ----------------------------------------------------------------------------------------------------------------
# Question 3


def check_findBall():
    """Tests findBall alone to see if it works"""
    print("Testing findBall...")
    print("----> Check visually <----")
    pic1 = cv2.imread("SampleImages/BallFinding/Blue1BG1Mid.jpg")
    pic2 = cv2.imread("SampleImages/BallFinding/Blue1BG3.jpg")
    pic3 = cv2.imread("SampleImages/BallFinding/Green1BG1Mid.jpg")
    pic4 = cv2.imread("SampleImages/BallFinding/Green1BG3.jpg")
    pic5 = cv2.imread("SampleImages/BallFinding/OrangeBG1Near.jpg")
    pic6 = cv2.imread("SampleImages/BallFinding/PinkBG1Mid.jpg")
    pic7 = cv2.imread("SampleImages/BallFinding/YellowBG1Mid.jpg")

    allPics = [pic1, pic2, pic3, pic4, pic5, pic6, pic7]
    picNames = ["blue1", "blue2", "green1", "green2", "orange", "pink", "yellow"]
    ballLocs = [(553, 278, 100), (400, 452, 65), (717, 296, 71), (532, 463, 63),
                (520, 262, 243), (890, 287, 78), (629, 350, 78)]
    for i in range(len(allPics)):
        name = picNames[i]
        pic = allPics[i]
        ballLoc = ballLocs[i]
        im, lb, ub, center, radius = hw3.findBall(pic)
        print(name, lb, ub, center, radius)
        if abs(center[0] - ballLoc[0]) < 10 and abs(center[1] - ballLoc[1]) < 10 and abs(radius - ballLoc[2]) < 10:
            print(name, ": close enough!")
        else:
            print(name, ": Not close enough")


# ----------------------------------------------------------------------------------------------------------------
# Question 5

def check_camshift2():
    """Tests camshift2"""
    print("Testing camshift2...")
    print("-------------Must Check Visually By Hand!-------------")
    blueRef = cv2.imread("SampleImages/refPics/refBlue.png")
    greenRef = cv2.imread("SampleImages/refPics/refGreen.png")
    pinkRef = cv2.imread("SampleImages/refPics/refPink.jpg")

    hw3.camshift2(blueRef, pinkRef)
    hw3.camshift2(greenRef, blueRef)
    hw3.camshift2(pinkRef, greenRef)


# ----------------------------------------------------------------------------------------------------------------
# Question 6


def check_videoVibe():
    """Tests videoVibe"""
    print("Testing videoVibe...")
    print("----> Must check visually! <----")

    hw3.videoVibe(0)
    hw3.videoVibe("SampleImages/People - 6387.mp4")
    hw3.videoVibe("SampleImages/Parrot - 9219.mp4")
    hw3.videoVibe("SampleImages/CarsStreet.avi")


# ==========================================================================================
# Main script, calls main function

runTests()
