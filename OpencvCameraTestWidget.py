import sys

import cv2
from PyQt4.QtCore import QTimer, Qt
from PyQt4.QtGui import QHBoxLayout, QLabel, QPixmap, QImage, QApplication, QWidget, QVBoxLayout, QSlider, QComboBox, \
    QFrame, QCheckBox, QLayout


class QImageWidget(QWidget):

    def __init__(self, parent=None):
        super(QImageWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.label = QLabel()
        self.label.setFrameShape(QFrame.Panel)
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(3)
        self.layout.addWidget(self.label)
        self.pixmap = QPixmap()
        self.label.setPixmap(self.pixmap)
        self.image = QImage()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

    def set_opencv_image(self, raw_image):
        if raw_image is not None:
            self.image = QImage(raw_image, raw_image.shape[1], \
                                raw_image.shape[0], raw_image.shape[1] * 3,
                                QImage.Format_RGB888)
            self.pixmap = QPixmap(self.image)
            self.label.setPixmap(self.pixmap)

    def show_on_second_screen(self):
        desktop_widget = QApplication.desktop()
        if desktop_widget.screenCount() > 1:
            second_screen_size = desktop_widget.screenGeometry(1)
            self.move(second_screen_size.left(), second_screen_size.top())
            self.resize(second_screen_size.width(), second_screen_size.height())
            self.showMaximized()


class OpencvCameraTestWidget(QWidget):
    available_resolutions = {"160x120": [160, 120], "176x144": [176, 144], "320x240": [320, 240], "352x288": [352, 288],
                             "640x480": [640, 480], "960x720": [960, 720], "1280x960": [1280, 960]}

    def __init__(self, parent=None, capture=None, widget=None):
        super(OpencvCameraTestWidget, self).__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)
        if capture is None:
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture = capture

        if widget is None:
            self.camera_widget = QImageWidget()
            self.main_layout.addWidget(self.camera_widget)

            self.camera_ret = 0
            self.raw_camera_image = None
            # cv2.namedWindow("image")

            self.camera_timer = QTimer()
            self.camera_timer.timeout.connect(self.grab_video)
            self.camera_timer.start(1000 / 24)

        self.brightness_layout = QHBoxLayout()
        self.brightness_label = QLabel("Brightness: ")
        self.brightness_layout.addWidget(self.brightness_label)
        self.brightness_value_label = QLabel("")
        self.brightness_value_label.setMinimumWidth(30)

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setFocusPolicy(Qt.StrongFocus)
        self.brightness_slider.setTickPosition(QSlider.TicksBothSides)
        self.brightness_slider.setMinimum(-10)
        self.brightness_slider.setMaximum(110)
        self.brightness_slider.setValue(20)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.valueChanged.connect(self.set_brightness)
        self.brightness_layout.addWidget(self.brightness_slider)
        self.brightness_layout.addWidget(self.brightness_value_label)
        self.main_layout.addLayout(self.brightness_layout)

        self.contrast_layout = QHBoxLayout()
        self.contrast_label = QLabel("Contrast: ")
        self.contrast_layout.addWidget(self.contrast_label)
        self.contrast_value_label = QLabel("")
        self.contrast_value_label.setMinimumWidth(30)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setFocusPolicy(Qt.StrongFocus)
        self.contrast_slider.setTickPosition(QSlider.TicksBothSides)
        self.contrast_slider.setMinimum(-10)
        self.contrast_slider.setMaximum(110)
        self.contrast_slider.setValue(20)
        self.contrast_slider.setTickPosition(QSlider.TicksBelow)
        self.contrast_slider.setTickInterval(10)
        self.contrast_slider.valueChanged.connect(self.set_contrast)
        self.contrast_layout.addWidget(self.contrast_slider)
        self.contrast_layout.addWidget(self.contrast_value_label)
        self.main_layout.addLayout(self.contrast_layout)

        self.exposure_layout = QHBoxLayout()
        self.exposure_label = QLabel("Exposure: ")
        self.exposure_layout.addWidget(self.exposure_label)
        self.exposure_value_label = QLabel("")
        self.exposure_value_label.setMinimumWidth(30)

        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setFocusPolicy(Qt.StrongFocus)
        self.exposure_slider.setTickPosition(QSlider.TicksBothSides)
        self.exposure_slider.setMinimum(-10)
        self.exposure_slider.setMaximum(110)
        self.exposure_slider.setValue(20)
        self.exposure_slider.setTickPosition(QSlider.TicksBelow)
        self.exposure_slider.setTickInterval(10)
        self.exposure_slider.valueChanged.connect(self.set_exposure)
        self.exposure_layout.addWidget(self.exposure_slider)
        self.exposure_layout.addWidget(self.exposure_value_label)
        self.main_layout.addLayout(self.exposure_layout)

        self.iso_layout = QHBoxLayout()
        self.iso_label = QLabel("ISO: ")
        self.iso_layout.addWidget(self.iso_label)
        self.iso_value_label = QLabel("")
        self.iso_value_label.setMinimumWidth(30)

        self.iso_slider = QSlider(Qt.Horizontal)
        self.iso_slider.setFocusPolicy(Qt.StrongFocus)
        self.iso_slider.setTickPosition(QSlider.TicksBothSides)
        self.iso_slider.setMinimum(-10)
        self.iso_slider.setMaximum(110)
        self.iso_slider.setValue(20)
        self.iso_slider.setTickPosition(QSlider.TicksBelow)
        self.iso_slider.setTickInterval(10)
        self.iso_slider.valueChanged.connect(self.set_iso)
        self.iso_layout.addWidget(self.iso_slider)
        self.iso_layout.addWidget(self.iso_value_label)
        self.main_layout.addLayout(self.iso_layout)

        self.auto_exposure_label = QLabel("AutoExposure: ")
        self.auto_exposure_checkbox = QCheckBox("AutoExposure: ")
        self.exposure_layout.addWidget(self.auto_exposure_checkbox)
        self.auto_exposure_checkbox.stateChanged.connect(self.set_auto_exposure)

        self.resolutions_combo = QComboBox()
        self.resolutions_combo.addItems(self.available_resolutions.keys())
        self.main_layout.addWidget(self.resolutions_combo)
        self.resolutions_combo.currentIndexChanged[str].connect(self.set_resolution)

    def set_brightness(self, value):
        self.capture.set(cv2.CAP_PROP_BRIGHTNESS, value / 100.0)
        self.brightness_value_label.setText(str(value / 100.0))

    def set_contrast(self, value):
        self.capture.set(cv2.CAP_PROP_CONTRAST, value / 100.0)
        self.contrast_value_label.setText(str(value / 100.0))

    def set_exposure(self, value):

        self.capture.set(cv2.CAP_PROP_EXPOSURE, value / 100.0)
        self.exposure_value_label.setText(str(value / 100.0))

    def set_iso(self, value):

        self.capture.set(cv2.CAP_PROP_ISO_SPEED, value / 100.0)
        self.exposure_value_label.setText(str(value / 100.0))

    def set_auto_exposure(self, value):
        if value > 0:
            self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        else:
            self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)

    def set_resolution(self, string):
        if str(string) in self.available_resolutions:
            height = self.available_resolutions[str(string)][0]
            width = self.available_resolutions[str(string)][1]
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def grab_video(self):
        # print "grab video"
        self.camera_ret, self.raw_camera_image = self.capture.read()
        if self.camera_ret:
            self.raw_camera_image = cv2.cvtColor(self.raw_camera_image, cv2.COLOR_BGR2RGB)
            self.camera_widget.set_opencv_image(self.raw_camera_image)


def main():
    app = QApplication([])
    # desktop_widget = QApplication.desktop()
    # print desktop_widget.screenCount()
    # screen_resolution = app.desktop().screenGeometry()
    # print screen_resolution
    # width, height = screen_resolution.width(), screen_resolution.height()
    #
    control_panel = OpencvCameraTestWidget()
    control_panel.show()
    sys.exit(app.exec_())

    # game = ImageGame()
    # game.game_loop()


if __name__ == '__main__':
    main()
