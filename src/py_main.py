import sys
import numpy as np
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QAction, QColor, QContextMenuEvent, QMouseEvent, QPalette
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QHBoxLayout, QLabel, QMainWindow, QMenu, QPushButton, QSlider, QTabWidget, QVBoxLayout, QWidget
import pyqtgraph as pg


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


# Create a subclass for a dialog window that has buttons to accept or reject the dialog.
class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.setWindowTitle("Dialog")
        self.setModal(True)

        buttons = (QDialogButtonBox.StandardButton.Apply |
                   QDialogButtonBox.StandardButton.Ok |
                   QDialogButtonBox.StandardButton.Save |
                   QDialogButtonBox.StandardButton.Open |
                   QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Open another window?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


# Create a subclass for QMainWindow to create a custom window.
class Label(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        # Track the mouse movement even when no mouse button is pressed.
        self.setMouseTracking(True)
        # Center the text in the label widget.
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse move event at (" + str(event.pos().x()) + ", " + str(event.pos().y()) + ")")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse press event: " + str(event.button()))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse release event: " + str(event.button()))
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.setText("Mouse double click event: " + str(event.button()))
        super().mouseDoubleClickEvent(event)


# Create a subclass for pg.PlotWidget to handle mouse events.
class PlotWidget(pg.PlotWidget):
    def __init__(self, getLayoutMargins):
        super().__init__()
        self.getLayoutMargins = getLayoutMargins
        self.setMouseTracking(True)
        self.last_clicked = 'end'
        self.start = np.zeros(2, dtype=float)
        self.end = np.zeros(2, dtype=float)
        self.n_steps = 10
        self.pen = pg.mkPen(color=QColor(240, 240, 240), width=2, style=Qt.PenStyle.SolidLine)
        self.viewbox = self.getViewBox()
        self.viewbox.setRange(xRange=[0, 1000], yRange=[0, 1000], padding=0)
        self.viewbox.setAspectLocked(False)
        self.viewbox.setMouseEnabled(x=False, y=False)  # Disable mouse interaction to avoid interference
        self.plotItem = self.getPlotItem()
        self.plotItem.setMouseEnabled(x=False, y=False)  # Disable mouse interaction to avoid interference
        self.plotItem.showGrid(x=True, y=True, alpha=0.3)  # Optional: Show grid for better visualization
        self.plotItem.setContentsMargins(0, 0, 0, 0)  # Ensure no margins around the plot area

    def mousePressEvent(self, event: QMouseEvent) -> None:
        " Capture the mouse event, update the graph, and the pass the event up."
        print("Clicked the graph")
        self.update_graph(event)
        super().mousePressEvent(event)

    def update_graph(self, event=None):
        " Update the graph with a new trajectory "
        # Check if the event is a left mouse button press event.
        if event is not None and event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos().toPointF()
            print(f"Mouse click at ({pos.x()}, {pos.y()})")
            # Get the geometries
            viewbox_geom = self.viewbox.geometry()
            plot_geom = self.geometry()

            # Calculate the width of the axes
            print(f"Layout margins: {self.getLayoutMargins()}")
            left_axis_width = viewbox_geom.left() - plot_geom.left() + self.getLayoutMargins()[0]
            # bottom_axis_height = plot_geom.bottom() - viewbox_geom.bottom()
            # bottom_axis_height = self.getLayoutMargins()[3]

            print(f"ViewBox Geometry: {viewbox_geom}")
            print(f"Plot Geometry: {plot_geom}")
            print(f"Left Axis Width: {left_axis_width}")

            # Adjust the position by the width of the axes
            adjusted_pos = pos - QPointF(left_axis_width, 0)
            print(f"Adjusted Mouse click at ({adjusted_pos.x()}, {adjusted_pos.y()})")

            data_pos = self.viewbox.mapToView(adjusted_pos)
            data_x = data_pos.x()
            data_y = data_pos.y()
            print(f"Data position: ({data_x}, {data_y})")
            print(f"Data position types: ({type(data_x)}, {type(data_y)})")
            if self.last_clicked == 'start':
                self.end[:] = [data_x, data_y]
                self.last_clicked = 'end'
            else:
                self.start[:] = [data_x, data_y]
                self.last_clicked = 'start'
        print(f"Start: {self.start[0]}, {self.start[1]}")
        print(f"End: {self.end[0]}, {self.end[1]}")
        self.x_data = np.linspace(self.start[0], self.end[0], self.n_steps)
        self.y_data = np.linspace(self.start[1], self.end[1], self.n_steps)
        self.plot(self.x_data, self.y_data, pen=self.pen, symbol='x', symbolSize=10, symbolBrush=QColor('blue'), symbolPen=None, clear=True)
        self.plot([self.x_data[0]], [self.y_data[0]], pen=None, symbol='o', symbolBrush='g', symbolSize=15)
        self.plot([self.x_data[-1]], [self.y_data[-1]], pen=None, symbol='o', symbolBrush='r', symbolSize=15)

        # Prevent autoscaling of the graph after updating the graph.
        self.viewbox.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=False)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Set window properties.
        self.setWindowTitle("Real-Time Trajectories")
        self.setAutoFillBackground(True)
        palette = self.palette()
        color = QColor(20, 20, 100)
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        self.setMouseTracking(True)

        # The window is split into two main sections; controls on the left, and a graph on the right.
        # The left side will consist of tabs for different types of controls, with the tabs implemented by QTabWidget.

        # Add a layout for the left side of the window
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setTabShape(QTabWidget.TabShape.Rounded)

        layout_left_tab1 = QVBoxLayout()

        widget = Label("Put the mouse in this window.")
        widget.setMouseTracking(True)
        widget.setAutoFillBackground(True)
        widget.setStyleSheet("background-color: rgb(100, 100, 100)")
        layout_left_tab1.addWidget(widget)

        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout_left_tab1.addWidget(widget)

        widget = QCheckBox()
        widget.setCheckState(Qt.CheckState.Checked)
        widget.stateChanged.connect(self.show_state)
        layout_left_tab1.addWidget(widget)

        widget = QPushButton("Click me")
        widget.clicked.connect(self.open_dialog)
        layout_left_tab1.addWidget(widget)

        widget_left_tab1 = QWidget()
        widget_left_tab1.setLayout(layout_left_tab1)
        tabs.addTab(widget_left_tab1, "Tab 1")

        layout_left_tab2 = QVBoxLayout()

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])
        widget.currentTextChanged.connect(lambda i: print(i))
        layout_left_tab2.addWidget(widget)

        widget = QDoubleSpinBox()
        widget.setRange(-10, 10)
        widget.setSingleStep(0.01)
        widget.lineEdit().setReadOnly(True)
        widget.valueChanged.connect(lambda i: print(f'%.2f' % i))
        layout_left_tab2.addWidget(widget)

        widget = QSlider()
        widget.setOrientation(Qt.Orientation.Horizontal)
        widget.setRange(0, 100)
        widget.setSingleStep(5)
        widget.setValue(20)
        widget.valueChanged.connect(lambda i: print(i))
        layout_left_tab2.addWidget(widget)

        widget_left_tab2 = QWidget()
        widget_left_tab2.setLayout(layout_left_tab2)
        tabs.addTab(widget_left_tab2, "Tab 2")

        # Set properties of the layout on the left side of the window.
        tabs.setMinimumSize(400, 300)
        tabs.setMaximumSize(800, 600)
        tabs.setAutoFillBackground(True)
        palette = tabs.palette()
        color = (100, 20, 20)
        palette.setColor(QPalette.ColorRole.Window, QColor(*color))
        tabs.setPalette(palette)

        # Add a layout that can be used to display a graph on the right side of the window.
        self.layout_right = QVBoxLayout()
        print("Initial margins:", self.layout_right.getContentsMargins())
        # self.layout_right.setContentsMargins(0, 0, 0, 0)
        getLayoutMargins = self.layout_right.getContentsMargins
        self.graph = PlotWidget(getLayoutMargins)
        self.layout_right.addWidget(self.graph)
        print("Margins after adding graph widget:", self.layout_right.getContentsMargins())
        color = QColor(100, 100, 100, 200)
        self.graph.setBackground(color)
        self.graph.start[:] = np.array([0, 0])
        self.graph.end[:] = np.array([10, 10])
        self.graph.update_graph()

        # Set properties of the layout on the right side of the window.
        widget_right = QWidget()
        widget_right.setLayout(self.layout_right)
        widget_right.setMinimumSize(400, 300)
        widget_right.setMaximumSize(800, 600)
        widget_right.setStyleSheet("background-color: rgb(20, 100, 20)")
        widget_right.setMouseTracking(True)
        print("Margins after setting layout to widget_right:", self.layout_right.getContentsMargins())

        # Add the left and right layouts to the main layout of the window.
        layout_main = QHBoxLayout()
        layout_main.addWidget(tabs)
        layout_main.addWidget(widget_right)
        layout_main.setSpacing(10)

        # Set the central widget of the window.
        widget_main = QWidget()
        widget_main.setLayout(layout_main)
        self.setCentralWidget(widget_main)

        # Set the window size.
        self.resize(1000, 600)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1600, 1200)
        print("Margins at the end of __init__:", self.layout_right.getContentsMargins())

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        " Create a custom context menu. "
        # Create a context menu.
        context_menu = QMenu(self)
        # Add an action to the context menu.
        action = QAction("Exit", self)
        # Connect the action to the exit() method.
        action.triggered.connect(QApplication.quit)
        # Add the action to the context menu.
        context_menu.addAction(action)
        # Execute the context menu.
        context_menu.exec(event.globalPos())

    def open_dialog(self):
        " Open a dialog window. "
        dialog = CustomDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            print('Accepted')
            self.w = AnotherWindow()
            self.w.show()
        else:
            print('Canceled')
            if self.w is not None:
                self.w.close()
            else:
                self.w = None

    def show_state(self, state):
        " Print the state of the checkbox. "
        print(f"Checkbox state: {state}")


if __name__ == "__main__":
    # Create an application. This contains the main event loop; it is required to run any PyQt program.
    app = QApplication(sys.argv)
    # Create a window. The parent of the window is None.
    window = MainWindow()
    # A window without a parent is not displayed. The window is displayed by calling the show() method.
    window.show()
    # Call the QApplication.exec() method to start the event loop.
    app.exec()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle("PyQtGraph Example")
#         self.setGeometry(100, 100, 800, 600)
#         self.plot_widget = PlotWidget()
#         self.setCentralWidget(self.plot_widget)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())