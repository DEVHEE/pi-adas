import cv2
import numpy as np


def thresholding(img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([80, 0, 0])
    upperWhite = np.array([255, 160, 255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    return maskWhite


def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp


def nothing(i):
    pass


def initializeTrackbars(intialTracbarVals, wt=720, ht=360):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 540, 360)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0], wt//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], ht, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2], wt//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], ht, nothing)


def valTrackbars(wt=720, ht=360):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wt - widthTop, heightTop),
                         (widthBottom, heightBottom), (wt - widthBottom, heightBottom)])
    return points


def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img


def getHistogram(img, minPer=0.1, display=False):
    hisValues = np.sum(img, axis=0)
    print(hisValues)
    maxValue = np.max(hisValues)
    minValue = minPer * maxValue

    indexArray = np.where(hisValues >= minValue)
    basePoint = int(np.average(indexArray))
    print(basePoint)

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(hisValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0] - intensity//255), (255, 0, 255), 1)
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return basePoint, imgHist
    return basePoint
