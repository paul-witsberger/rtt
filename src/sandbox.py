from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication
import sys

class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Change the background color of the layout for demonstration purposes
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: lightblue;")
        # Set some margins for demonstration purposes
        self.layout.setContentsMargins(10, 20, 30, 40)
        widget = QWidget()
        widget.setStyleSheet("background-color: lightcoral;")
        self.layout.addWidget(widget)

    def get_layout_padding(self):
        left, top, right, bottom = self.layout.getContentsMargins()
        print(f"Left: {left}, Top: {top}, Right: {right}, Bottom: {bottom}")
        return left, top, right, bottom

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ExampleWidget()
    widget.show()
    widget.get_layout_padding()
    sys.exit(app.exec())