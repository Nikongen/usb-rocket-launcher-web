import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Webcam App")
        self.setGeometry(100, 100, 640, 480)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.video_capture = cv2.VideoCapture(0)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Draw crosshair on the frame
            height, width, _ = frame.shape
            cv2.line(frame, (width // 2, 0), (width // 2, height), (255, 0, 0), 1)
            cv2.line(frame, (0, height // 2), (width, height // 2), (255, 0, 0), 1)
            
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec_())
