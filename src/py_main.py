from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import sys

# Create a subclass for QMainWindow to create a custom window.
class Label(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse move event at (" + str(event.pos().x()) + ", " + str(event.pos().y()) + ")")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse press event: " + str(event.button()))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse release event")

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse double click event")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.label = QLabel("Click in this window")
        self.label = Label("Click in this window")

        # Set the central widget of the window.
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, event) -> None:
        self.label.setText("Mouse move event")

    def mousePressEvent(self, event) -> None:
        self.label.setText("Mouse press event")

    def mouseReleaseEvent(self, event) -> None:
        self.label.setText("Mouse release event")

    def mouseDoubleClickEvent(self, event) -> None:
        self.label.setText("Mouse double click event")

# Create an application. This contains the main event loop; it is required to run any PyQt program.
app = QApplication(sys.argv)
# Create a window. The parent of the window is None.
window = MainWindow()
# A window without a parent is not displayed. The window is displayed by calling the show() method.
window.show()
# Call the QApplication.exec() method to start the event loop.
app.exec()