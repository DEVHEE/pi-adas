# import processing
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
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp


def nothing(i):
    pass


def initializeTrackbars(initTrackbarVals, wT, hT):
    cv2.namedWindow("Adjust Area")
    cv2.createTrackbar("Width Top", "Adjust Area", initTrackbarVals[0], wT//2, nothing)
    cv2.createTrackbar("Height Top", "Adjust Area", initTrackbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Adjust Area", initTrackbarVals[2], wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Adjust Area", initTrackbarVals[3], hT, nothing)


def valTrackbars(wT, hT):
    widthTop = cv2.getTrackbarPos("Width Top", "Adjust Area")
    heightTop = cv2.getTrackbarPos("Height Top", "Adjust Area")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Adjust Area")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Adjust Area")
    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop),
                         (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])
    return points


def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 10, (0, 0, 255), cv2.FILLED)
    return img


def getHistogram(img, minPer=0.1, display=False, region=1):

    if region == 1:
        hisValues = np.sum(img, axis=0)
    else:
        hisValues = np.sum(img[img.shape[0]//region:, :], axis=0)
    # print(hisValues)
    maxValue = np.max(hisValues)
    minValue = minPer * maxValue

    indexArray = np.where(hisValues >= minValue)
    basePoint = int(np.average(indexArray))
    # print(basePoint)

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(hisValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0] - intensity//255//region), (255, 0, 255), 1)
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return basePoint, imgHist
    return basePoint


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

