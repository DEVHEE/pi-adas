# import modules
import cv2
import numpy as np
import utils

curveList = []
avgVal = 10


def getLaneCurve(img, display=2):
    imgCopy = img.copy()
    imgResult = img.copy()

    imgThres = utils.thresholding(img)

    hT, wT, c = img.shape
    points = utils.valTrackbars(vidWidth, vidHeight)
    # print(points[0], points[2])
    imgWrap = utils.warpImg(imgThres, points, wT, hT)
    imgWrapPoints = utils.drawPoints(imgCopy, points)

    middlePoint, imgHist = utils.getHistogram(imgWrap, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utils.getHistogram(imgWrap, display=True, minPer=0.5)
    curveRaw = curveAveragePoint - middlePoint

    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    if display != 0:
        imgInvWarp = utils.warpImg(imgWrap, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)

    if display == 2:
        imgStacked = utils.stackImages(0.7, ([img, imgWrapPoints, imgWrap],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('Image Processing', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)
    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture("sample.mp4")
    vidWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vidHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    initialTrackBarVals = [147, 117, 68, 320]
    utils.initializeTrackbars(initialTrackBarVals, vidWidth, vidHeight)
    frameCounter = 0
    curveList = []

    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        img = cv2.resize(img, (vidWidth, vidHeight))
        curve = getLaneCurve(img, display=2)
        # print(curve)
        # cv2.imshow('vid', img)
        cv2.waitKey(1)
