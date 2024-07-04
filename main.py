import cv2
import numpy as np
import utils


def getLaneCurve(img):

    imgCopy = img.copy()

    imgThres = utils.thresholding(img)

    h, w, c = img.shape
    points = utils.valTrackbars()
    print(points[0], points[2])
    imgWrap = utils.warpImg(imgThres, points, w, h)
    imgWrapPoints = utils.drawPoints(imgCopy, points)

    basePoint, imgHist = utils.getHistogram(imgWrap, display=True)

    cv2.imshow('Thres', imgThres)
    cv2.imshow('Warp', imgWrap)
    cv2.imshow('Warp Points', imgWrapPoints)
    cv2.imshow('Histogram', imgHist)
    return None


if __name__ == '__main__':
    cap = cv2.VideoCapture("sample.mp4")
    vidWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vidHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    initialTrackBarVals = [147, 117, 68, 320]
    utils.initializeTrackbars(initialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        img = cv2.resize(img, (vidWidth, vidHeight))
        getLaneCurve(img)
        cv2.imshow('vid', img)
        cv2.waitKey(1)