import copy
import pickle
import subprocess
import sys

import cv2
import numpy as np
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication, QWidget, QVBoxLayout, QPushButton, QPixmap, QLabel, QImage, QHBoxLayout

import apriltag


class ImageGame():

    def __init__(self, width=848, height=477):

        self.refPts = []
        self.origPts = []
        self.state = 0
        self.W = width  # 424
        self.H = height  # 238
        self.framesTag = 0
        self.positionTag = -1
        self.detector = apriltag.Detector()

        self.img1 = cv2.imread('resources/1.jpg')
        self.img2 = cv2.imread('resources/2.jpg')
        self.img3 = cv2.imread('resources/3.jpg')
        self.img4 = cv2.imread('resources/4.jpg')
        cv2.namedWindow("image")
        cv2.namedWindow("camera")
        self.refImage = np.array(np.zeros((self.H, self.W, 3)), dtype=np.uint8)
        self.refImage[:] = (255, 255, 255)
        self.capture = cv2.VideoCapture(0)
        self.calibration_state = -1
        # cv2.imshow("1", self.img1)
        # cv2.imshow("2", self.img2)
        # cv2.imshow("3", self.img3)
        # cv2.imshow("4", self.img4)

    def init_clicks(self):
        # Draw a circle to be clicked
        # self.refImage = np.array(np.zeros((self.H, self.W, 3)), dtype=np.uint8)
        # self.copyRoi(self.refImage, self.april_1, 10, 10)
        # self.copyRoi(self.refImage, self.april_1, self.H - self.april_1.shape[0] - 10, 10)
        # self.copyRoi(self.refImage, self.april_1, 10, self.W - self.april_1.shape[1] - 10)
        # self.copyRoi(self.refImage, self.april_1, self.H - self.april_1.shape[0] - 10,
        #              self.W - self.april_1.shape[1] - 10)
        # cv2.circle(self.refImage, (5, 5), 5, (255, 0, 0), -1)
        cv2.setMouseCallback("camera", self.clickkk)
        # cv2.setMouseCallback("image", self.calibrate)

    def clickkk(self, event, x, y, flags, param):
        a = []

        if self.state is not 0:
            return
        if event == cv2.EVENT_LBUTTONDOWN:
            self.calibration_state = 0
        #     self.origPts.append([5, 5])
        #     self.origPts.append([self.W, 5])
        #     self.origPts.append([5, self.H])
        #     self.origPts.append([self.W, self.H])
        #     ret, rgbImage = self.capture.read()
        #     gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
        #     xs = []
        #     ys = []
        #     detections, dimg = self.detector.detect(gray, return_image=True)
        #     if len(detections) == 4:
        #         for detection in detections:
        #             xs.append(detection.center[0])
        #             ys.append(detection.center[1])
        #     for coord in xrange(3):
        #         if xs[coord] == min(xs):
        #             if ys[coord] == min(ys):
        #                 self.origPts.append([5, 5])
        #                 self.refPts.append([xs[coord], ys[coord]])
        #             else:

        # if event == cv2.EVENT_LBUTTONDOWN:
        #     if len(self.origPts) == 0:
        #         self.origPts.append([5, 5])
        #         # Remove last circle
        #         cv2.circle(self.refImage, (5, 5), 5, (0, 0, 0), -1)
        #         # Draw a new circle to be clicked
        #         cv2.circle(self.refImage, (self.W, 5), 5, (255, 0, 0), -1)
        #     elif len(self.origPts) == 1:
        #         self.origPts.append([self.W, 5])
        #         # Remove last circle
        #         cv2.circle(self.refImage, (self.W, 5), 5, (0, 0, 0), -1)
        #         # Draw a new circle to be clicked
        #         cv2.circle(self.refImage, (self.W, self.H), 5, (255, 0, 0), -1)
        #     elif len(self.origPts) == 2:
        #         self.origPts.append([self.W, self.H])
        #         # Remove last circle
        #         cv2.circle(self.refImage, (self.W, self.H), 5, (0, 0, 0), -1)
        #         # Draw a new circle to be clicked
        #         cv2.circle(self.refImage, (5, self.H), 5, (255, 0, 0), -1)
        #     else:
        #         # Remove last circle
        #         cv2.circle(self.refImage, (5, self.H), 5, (0, 0, 0), -1)
        #         self.origPts.append([5, self.H])
        #     self.refPts.append([x, y])

    def init_interface(self):
        self.state = 0
        self.composeImage(self.refImage, self.img1, self.img2, self.img3, self.img4)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, rgbImage = self.capture.read()
        cv2.imshow("image", self.refImage)
        # try:
        #     cv2.imshow("perspective", perspective_image)
        # except:
        #     pass
        rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
        cv2.imshow("camera", rgbImage)
        k = cv2.waitKey(1)

    def calibrate(self):
        if self.calibration_state > 4 or self.calibration_state < 0:
            return
        self.refImage[:] = (255, 255, 255)
        april_0 = cv2.imread('resources/april_0.png')
        april_0 = cv2.resize(april_0, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        april_1 = cv2.imread('resources/april_1.png')
        april_1 = cv2.resize(april_1, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        april_2 = cv2.imread('resources/april_2.png')
        april_2 = cv2.resize(april_2, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        april_3 = cv2.imread('resources/april_3.png')
        april_3 = cv2.resize(april_3, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            if self.calibration_state == 0:
                self.copyRoi(self.refImage, april_0, 10, 10)
                ret, rgbImage = self.capture.read()
                gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
                detections, dimg = self.detector.detect(gray, return_image=True)
                if len(detections) == 1:
                    if detections[0].tag_id == 0:
                        self.origPts.append([5, 5])
                        self.refPts.append([detections[0].corners[0][0] - 2,
                                            detections[0].corners[0][1] - 2])
                        self.calibration_state = 1
                        self.refImage[:] = (255, 255, 255)
                        cv2.waitKey(1000)
            elif self.calibration_state == 1:
                self.copyRoi(self.refImage, april_1, self.H - april_1.shape[0] - 10, 10)
                ret, rgbImage = self.capture.read()
                gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
                detections, dimg = self.detector.detect(gray, return_image=True)
                if len(detections) == 1:
                    if detections[0].tag_id == 1:
                        self.origPts.append([5, self.H])
                        self.refPts.append([detections[0].corners[3][0] - 2,
                                            detections[0].corners[3][1] + 2])
                        self.calibration_state = 2
                        self.refImage[:] = (255, 255, 255)
                        cv2.waitKey(1000)
            elif self.calibration_state == 2:
                self.copyRoi(self.refImage, april_2, 10, self.W - april_2.shape[1] - 10)
                ret, rgbImage = self.capture.read()
                gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
                detections, dimg = self.detector.detect(gray, return_image=True)
                if len(detections) == 1:
                    if detections[0].tag_id == 2:
                        self.origPts.append([self.W, 5])
                        self.refPts.append([detections[0].corners[1][0] + 2,
                                            detections[0].corners[1][1] - 2])
                        self.calibration_state = 3
                        self.refImage[:] = (255, 255, 255)
                        cv2.waitKey(1000)
            elif self.calibration_state == 3:
                self.copyRoi(self.refImage, april_3, self.H - april_3.shape[0] - 10,
                             self.W - april_3.shape[1] - 10)
                ret, rgbImage = self.capture.read()
                gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
                detections, dimg = self.detector.detect(gray, return_image=True)
                if len(detections) == 1:
                    if detections[0].tag_id == 3:
                        self.origPts.append([self.W, self.H])
                        self.refPts.append([detections[0].corners[2][0] + 2,
                                            detections[0].corners[2][1] + 2])
                        self.calibration_state = 4
            elif self.calibration_state == 4:
                print "Calibration ended"
                break
            cv2.imshow("image", self.refImage)
            rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
            cv2.imshow("camera", rgbImage)
            k = cv2.waitKey(1)

        #
        #

    def toHomogeneous(self, p):
        ret = np.resize(p, (p.shape[0] + 1, 1))
        ret[-1][0] = 1.
        return ret

    def copyRoi(self, bigImage, small, row, col):
        # initial number of rows and columns
        rows = small.shape[0]
        cols = small.shape[1]
        # initial ending row/column value
        row2 = row + rows
        col2 = col + cols

        ## set rows
        # if row2 >= bigImage.shape[0]:
        # row2 = bigImage.shape[0]-1
        # rows = bigImage.shape[0]-1-row
        ## set col
        # if col2 >= bigImage.shape[1]:
        # col2 = bigImage.shape[1]-1
        # cols = bigImage.shape[1]-1-col

        # cv2.imwrite("caca.png", small[:rows, :cols, :])
        print 'big'
        print bigImage[row][col][0]
        print 'small'
        print small[0][0][0]
        print 'big'
        print bigImage[row][col][0]

        bigImage[row:row + rows, col:col + cols, :] = small[:rows, :cols, :]
        cv2.imwrite("resources/composed_image.png", bigImage)

    def composeImage(self, bigImage, small1, small2, small3, small4):
        # cv2.rectangle(bigImage, (0,0), (self.W/2, self.H/2), (255,0,0), -1)
        # cv2.rectangle(bigImage, (self.W/2,0), (self.W, self.H/2), (0,255,0), -1)
        # cv2.rectangle(bigImage, (self.W/2, self.H/2), (self.W, self.H), (0,0,255), -1)
        # cv2.rectangle(bigImage, (0,self.H/2), (self.W/2, self.H), (255,0,255), -1)
        self.copyRoi(bigImage, small1, 0, 0)
        self.copyRoi(bigImage, small2, 0, self.W / 2)
        self.copyRoi(bigImage, small3, self.H / 2, 0)
        self.copyRoi(bigImage, small4, self.H / 2, self.W / 2)

    def game_loop(self):

        self.init_clicks()

        try:
            print 'Trying to load calibration'
            h = pickle.load(open('h.pickle', 'r'))
            self.state = 1
            self.composeImage(self.refImage, self.img1, self.img2, self.img3, self.img4)
        except:
            print 'Can\'t load calibration'
            self.state = 0
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while True:
            ret, rgbImage = self.capture.read()
            if not ret:
                break

            if self.state == 0:
                self.calibrate()
                if len(self.refPts) == 4:
                    h, _ = cv2.findHomography(np.array(self.refPts), np.array(self.origPts))
                    try:
                        print 'Saving calibration'
                        pickle.dump(h, open('h.pickles', 'w'))
                        self.composeImage(self.refImage, self.img1, self.img2, self.img3, self.img4)
                    except:
                        print 'Can\'t save calibration'
                    self.state = 1
            elif self.state == 1:
                perspective_image = cv2.warpPerspective(rgbImage, h, (self.W, self.H))
                gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
                detections, dimg = self.detector.detect(gray, return_image=True)
                if len(detections) == 0:
                    self.framesTag -= 1
                    if self.framesTag == -1: self.framesTag = 0
                    if self.framesTag < -20: self.framesTag = -20
                else:
                    if detections[0].tag_id == 31:
                        for detection in detections:
                            p = self.toHomogeneous(detection.center)
                            p = np.dot(h, p)
                            print p
                            if p[0] < self.W / 2:
                                if p[1] < self.H / 2:
                                    pos = 1
                                else:
                                    pos = 3
                            else:
                                if p[1] < self.H / 2:
                                    pos = 2
                                else:
                                    pos = 4

                            if pos == self.positionTag:
                                self.framesTag += 1
                            else:
                                self.positionTag = pos
                                self.framesTag = 0

                            if self.framesTag > 20:
                                good = False
                                caca = copy.deepcopy(self.refImage)
                                if self.positionTag == 1:
                                    cv2.rectangle(caca, (0, 0), (self.W / 2, self.H / 2), (0, 0, 255, 20), -1)
                                elif self.positionTag == 2:
                                    cv2.rectangle(caca, (self.W / 2, 0), (self.W, self.H / 2), (0, 0, 255, 20), -1)
                                elif self.positionTag == 3:
                                    cv2.rectangle(caca, (0, self.H / 2), (self.W / 2, self.H), (0, 0, 255, 20), -1)
                                else:
                                    cv2.rectangle(caca, (self.W / 2, self.H / 2), (self.W, self.H), (0, 255, 0, 20), -1)
                                    good = True

                                if good:
                                    subprocess.Popen(["mplayer", "./resources/success.mp3"])
                                    cv2.circle(caca, (self.W / 2, self.H / 2), self.H / 5, (0, 255, 0), 10)

                                else:
                                    subprocess.Popen(["mplayer", "./resources/error.mp3"])
                                    cv2.line(caca, ((self.W / 2) - 200, (self.H / 2) - 200),
                                             ((self.W / 2) + 200, (self.H / 2) + 200), (0, 0, 255), 10)
                                    cv2.line(caca, ((self.W / 2) - 200, (self.H / 2) + 200),
                                             ((self.W / 2) + 200, (self.H / 2) - 200), (0, 0, 255), 10)

                                cv2.imshow("image", caca)
                                k = cv2.waitKey(1000)

                                self.framesTag = -20
                            print self.positionTag, self.framesTag
            else:
                print 'WTF'

            cv2.imshow("image", self.refImage)
            try:
                cv2.imshow("perspective", perspective_image)
            except:
                pass
            rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
            cv2.imshow("camera", rgbImage)
            k = cv2.waitKey(1)
            if k == 27 or k == 1048603:
                sys.exit(-1)


class ControlWidget(QWidget):
    def __init__(self, parent=None, width=848, height=477):
        super(ControlWidget, self).__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.calibration_button = QPushButton("Calibrate")
        self.calibration_button.clicked.connect(self.calibrate)
        self.main_layout.addWidget(self.calibration_button)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        self.images_layout = QHBoxLayout()
        self.camera_image = None
        self.camera_pixmap = QPixmap()
        self.camera_container = QLabel("Camera")
        self.camera_container.setPixmap(self.camera_pixmap)
        self.perspective_pixmap = QPixmap()
        self.perspective_container = QLabel("Perspective")
        self.perspective_container.setPixmap(self.perspective_pixmap)
        self.images_layout.addWidget(self.camera_container)
        self.images_layout.addWidget(self.perspective_container)
        self.main_layout.addLayout(self.images_layout)

        self.state = 0
        self.refPts = []
        self.origPts = []
        self.state = 0
        self.W = width  # 424
        self.H = height  # 238
        self.framesTag = 0
        self.positionTag = -1
        self.detector = apriltag.Detector()

        self.img1 = cv2.imread('resources/1.jpg')
        self.img2 = cv2.imread('resources/2.jpg')
        self.img3 = cv2.imread('resources/3.jpg')
        self.img4 = cv2.imread('resources/4.jpg')
        self.refImage = np.array(np.zeros((self.H, self.W, 3)), dtype=np.uint8)
        self.refImage[:] = (255, 255, 255)
        self.calibration_state = 0
        self.camera_ret = 0
        self.raw_camera_image = None
        cv2.namedWindow("image")

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.grab_video)
        self.camera_timer.start(1000 / 24)
        self.processing_timer = QTimer()
        self.processing_timer.timeout.connect(self.game_loop)
        self.processing_timer.start(1000 / 24)

    def grab_video(self):
        self.camera_ret, self.raw_camera_image = self.capture.read()
        if self.camera_ret:
            self.raw_camera_image = cv2.cvtColor(self.raw_camera_image, cv2.COLOR_BGR2RGB)
            self.camera_image = QImage(self.raw_camera_image, self.raw_camera_image.shape[1], \
                                       self.raw_camera_image.shape[0], self.raw_camera_image.shape[1] * 3,
                                       QImage.Format_RGB888)
            self.camera_pixmap = QPixmap(self.camera_image)
            self.camera_container.setPixmap(self.camera_pixmap)

    def calibrate(self):
        if self.calibration_state > 4 or self.calibration_state < 0:
            return
        self.refImage[:] = (255, 255, 255)
        april_0 = cv2.imread('resources/april_0.png')
        april_0 = cv2.resize(april_0, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        april_1 = cv2.imread('resources/april_1.png')
        april_1 = cv2.resize(april_1, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        april_2 = cv2.imread('resources/april_2.png')
        april_2 = cv2.resize(april_2, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        april_3 = cv2.imread('resources/april_3.png')
        april_3 = cv2.resize(april_3, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            gray = cv2.cvtColor(self.raw_camera_image, cv2.COLOR_BGR2GRAY)
            if self.calibration_state == 0:
                self.copyRoi(self.refImage, april_0, 10, 10)

            elif self.calibration_state == 1:
                self.copyRoi(self.refImage, april_1, self.H - april_1.shape[0] - 10, 10)

            elif self.calibration_state == 2:
                self.copyRoi(self.refImage, april_2, 10, self.W - april_2.shape[1] - 10)

            elif self.calibration_state == 3:
                self.copyRoi(self.refImage, april_3, self.H - april_3.shape[0] - 10,
                             self.W - april_3.shape[1] - 10)
            detections, dimg = self.detector.detect(gray, return_image=True)
            if len(detections) == 1:
                if detections[0].tag_id == 0:
                    self.origPts.append([5, 5])
                    self.refPts.append([detections[0].corners[0][0] - 2,
                                        detections[0].corners[0][1] - 2])
                    self.calibration_state = 1
                    self.refImage[:] = (255, 255, 255)
                    cv2.waitKey(1000)
                elif detections[0].tag_id == 1:
                    self.origPts.append([5, self.H])
                    self.refPts.append([detections[0].corners[3][0] - 2,
                                        detections[0].corners[3][1] + 2])
                    self.calibration_state = 2
                    self.refImage[:] = (255, 255, 255)
                    cv2.waitKey(1000)
                elif detections[0].tag_id == 2:
                    self.origPts.append([self.W, 5])
                    self.refPts.append([detections[0].corners[1][0] + 2,
                                        detections[0].corners[1][1] - 2])
                    self.calibration_state = 3
                    self.refImage[:] = (255, 255, 255)
                    cv2.waitKey(1000)
                elif detections[0].tag_id == 3:
                    self.origPts.append([self.W, self.H])
                    self.refPts.append([detections[0].corners[2][0] + 2,
                                        detections[0].corners[2][1] + 2])
                    self.calibration_state = 4
                    break
            cv2.imshow("image", self.refImage)
            k = cv2.waitKey(1)
        print "Calibration ended"

    def copyRoi(self, bigImage, small, row, col):
        # initial number of rows and columns
        rows = small.shape[0]
        cols = small.shape[1]
        # initial ending row/column value
        row2 = row + rows
        col2 = col + cols

        ## set rows
        # if row2 >= bigImage.shape[0]:
        # row2 = bigImage.shape[0]-1
        # rows = bigImage.shape[0]-1-row
        ## set col
        # if col2 >= bigImage.shape[1]:
        # col2 = bigImage.shape[1]-1
        # cols = bigImage.shape[1]-1-col

        # cv2.imwrite("caca.png", small[:rows, :cols, :])
        print 'big'
        print bigImage[row][col][0]
        print 'small'
        print small[0][0][0]
        print 'big'
        print bigImage[row][col][0]

        bigImage[row:row + rows, col:col + cols, :] = small[:rows, :cols, :]

    def game_loop(self):
        if self.state == 0:
            if len(self.refPts) == 4:
                h, _ = cv2.findHomography(np.array(self.refPts), np.array(self.origPts))
                try:
                    print 'Saving calibration'
                    pickle.dump(h, open('h.pickles', 'w'))
                    self.composeImage(self.refImage, self.img1, self.img2, self.img3, self.img4)
                except:
                    print 'Can\'t save calibration'
                self.state = 1
        elif self.state == 1:
            perspective_image = cv2.warpPerspective(self.raw_camera_image, h, (self.W, self.H))
            gray = cv2.cvtColor(self.raw_camera_image, cv2.COLOR_BGR2GRAY)
            detections, dimg = self.detector.detect(gray, return_image=True)
            if len(detections) == 0:
                self.framesTag -= 1
                if self.framesTag == -1: self.framesTag = 0
                if self.framesTag < -20: self.framesTag = -20
            else:
                if detections[0].tag_id == 31:
                    for detection in detections:
                        p = self.toHomogeneous(detection.center)
                        p = np.dot(h, p)
                        print p
                        if p[0] < self.W / 2:
                            if p[1] < self.H / 2:
                                pos = 1
                            else:
                                pos = 3
                        else:
                            if p[1] < self.H / 2:
                                pos = 2
                            else:
                                pos = 4

                        if pos == self.positionTag:
                            self.framesTag += 1
                        else:
                            self.positionTag = pos
                            self.framesTag = 0

                        if self.framesTag > 20:
                            good = False
                            caca = copy.deepcopy(self.refImage)
                            if self.positionTag == 1:
                                cv2.rectangle(caca, (0, 0), (self.W / 2, self.H / 2), (0, 0, 255, 20), -1)
                            elif self.positionTag == 2:
                                cv2.rectangle(caca, (self.W / 2, 0), (self.W, self.H / 2), (0, 0, 255, 20), -1)
                            elif self.positionTag == 3:
                                cv2.rectangle(caca, (0, self.H / 2), (self.W / 2, self.H), (0, 0, 255, 20), -1)
                            else:
                                cv2.rectangle(caca, (self.W / 2, self.H / 2), (self.W, self.H), (0, 255, 0, 20), -1)
                                good = True

                            if good:
                                subprocess.Popen(["mplayer", "./resources/success.mp3"])
                                cv2.circle(caca, (self.W / 2, self.H / 2), self.H / 5, (0, 255, 0), 10)

                            else:
                                subprocess.Popen(["mplayer", "./resources/error.mp3"])
                                cv2.line(caca, ((self.W / 2) - 200, (self.H / 2) - 200),
                                         ((self.W / 2) + 200, (self.H / 2) + 200), (0, 0, 255), 10)
                                cv2.line(caca, ((self.W / 2) - 200, (self.H / 2) + 200),
                                         ((self.W / 2) + 200, (self.H / 2) - 200), (0, 0, 255), 10)

                            cv2.imshow("image", caca)
                            k = cv2.waitKey(1000)

                            self.framesTag = -20
                        print self.positionTag, self.framesTag
        else:
            print 'WTF'

        cv2.imshow("image", self.refImage)
        try:
            cv2.imshow("perspective", perspective_image)
        except:
            pass
        k = cv2.waitKey(1)
        if k == 27 or k == 1048603:
            sys.exit(-1)


class QSMImageGame():
    def __init__(self):
        # self.game = ImageGame()
        self.control_panel = ControlWidget()
        self.control_panel.show()

        # self.machine = QStateMachine()
        # self.states = {"init": None, "calibration": None, "waiting": None, "win": None, "loose": None, "end": None}
        # for state_name in self.states.keys():
        #     self.states[state_name] = QState()
        #     self.states[state_name].setObjectName(state_name)
        #     self.machine.addState(self.states[state_name])
        #
        # self.machine.addTransition(self.control_panel.calibration_button, SIGNAL('clicked()'),
        #                            self.states["calibration"])
        # self.states["calibration"].entered.connect(self.game.calibrate)
        # self.machine.setInitialState(self.states["calibration"])
        # self.machine.start()


def main():
    app = QApplication([])
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    the_game = QSMImageGame()
    sys.exit(app.exec_())

    # game = ImageGame()
    # game.game_loop()


if __name__ == '__main__':
    main()
