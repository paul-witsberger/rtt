import sys
import numpy as np
import pickle
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QAction, QColor, QContextMenuEvent, QMouseEvent, QPalette, QResizeEvent
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton, QSlider, QTabWidget, QVBoxLayout, QWidget
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


# Create a subclass for pg.PlotWidget to handle mouse events.
class PlotWidget(pg.PlotWidget):
    def __init__(self, parent, getLayoutMargins):
        super().__init__()
        self.parent = parent
        self.getLayoutMargins = getLayoutMargins
        self.setMouseTracking(True)
        self.last_clicked = 'end'
        self.start = np.array((self.parent.init_position[0]), dtype=float)
        self.end = np.array((self.parent.init_position[1]), dtype=float)
        self.n_steps = 10
        self.pen = pg.mkPen(color=QColor(100, 100, 255), width=2, style=Qt.PenStyle.SolidLine)
        self.viewbox = self.getViewBox()
        self.viewbox.setRange(xRange=[0, 1000], yRange=[0, 1000], padding=0)
        self.viewbox.setAspectLocked(True)
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True, alpha=0.3)  # Optional: Show grid for better visualization
        self.plot_initialized = False

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        event.ignore()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        " Update the graph when the mouse is moved. "
        if event.buttons() == Qt.MouseButton.LeftButton or event.buttons() == Qt.MouseButton.RightButton:
            self.update_graph(event)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        " Capture the mouse event, update the graph, and the pass the event up."
        self.update_graph(event)
        if event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.RightButton:
            event.ignore()
        else:
            super().mousePressEvent(event)

    def reload(self):
        self.plot_initialized = True
        self.start[:] = [self.x_data[0], self.y_data[0]]
        self.end[:] = [self.x_data[-1], self.y_data[-1]]
        self.plot(self.x_data, self.y_data, pen=self.pen, symbol='x', symbolSize=10, symbolBrush=QColor('white'), symbolPen=None, clear=True)
        self.plot([self.x_data[0]], [self.y_data[0]], pen=None, symbol='o', symbolBrush='g', symbolSize=15)
        self.plot([self.x_data[-1]], [self.y_data[-1]], pen=None, symbol='o', symbolBrush='r', symbolSize=15)
        self.viewbox.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=False)
        self.parent.update_position_label(self.start, self.end)

    def update_graph(self, event=None):
        " Update the graph with a new trajectory "
        is_updated = False
        # Check if the event is a left mouse button press event.
        if event is not None and (event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.RightButton or event.type() == QMouseEvent.Type.MouseMove):
            # Get the position of the mouse event. It must be a float so that the output is a QPointF.
            pos = event.pos().toPointF()
            # Get the geometries
            viewbox_geom = self.viewbox.geometry()
            plot_geom = self.geometry()
            # Calculate the width of the axes
            left_axis_width = viewbox_geom.left() - plot_geom.left() + self.getLayoutMargins()[0]
            # Adjust the position by the width of the axes
            adjusted_pos = pos - QPointF(left_axis_width, 1)
            # Convert the adjusted position to data coordinates
            data_pos = self.viewbox.mapToView(adjusted_pos)
            data_x = data_pos.x()
            data_y = data_pos.y()
            # Update the start or end point based on which mouse button is pressed.
            if event.button() == Qt.MouseButton.RightButton or (event.type() == QMouseEvent.Type.MouseMove and self.last_press == Qt.MouseButton.RightButton):
                self.last_press = Qt.MouseButton.RightButton
                self.end[:] = [data_x, data_y]
            elif event.button() == Qt.MouseButton.LeftButton or (event.type() == QMouseEvent.Type.MouseMove and self.last_press == Qt.MouseButton.LeftButton):
                self.last_press = Qt.MouseButton.LeftButton
                self.start[:] = [data_x, data_y]
            is_updated = True
        # Check if the user has entered new coordinates in the input fields.
        elif (self.parent.position_label_start_x.text() != '') and \
                (self.start[0] != float(self.parent.position_label_start_x.text()) or \
                self.start[1] != float(self.parent.position_label_start_y.text()) or \
                self.end[0] != (self.parent.position_label_end_x.text()) or\
                self.end[1] != (self.parent.position_label_end_y.text())):
            self.start[:] = [float(self.parent.position_label_start_x.text()), float(self.parent.position_label_start_y.text())]
            self.end[:] = [float(self.parent.position_label_end_x.text()), float(self.parent.position_label_end_y.text())]
            is_updated = True

        # Only update the graph if the coordinates have changed.
        if is_updated or not self.plot_initialized:
            self.x_data = np.linspace(self.start[0], self.end[0], self.n_steps)
            self.y_data = np.linspace(self.start[1], self.end[1], self.n_steps)
            self.plot(self.x_data, self.y_data, pen=self.pen, symbol='x', symbolSize=10, symbolBrush=QColor('white'), symbolPen=None, clear=True)
            self.plot([self.x_data[0]], [self.y_data[0]], pen=None, symbol='o', symbolBrush='g', symbolSize=15)
            self.plot([self.x_data[-1]], [self.y_data[-1]], pen=None, symbol='o', symbolBrush='r', symbolSize=15)
            self.plot_initialized = True
            # Prevent autoscaling of the graph after updating the graph.
            self.viewbox.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=False)
            self.parent.update_position_label(self.start, self.end)


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
        self.init_position = ([250, 250], [750, 750])

        # The window is split into two main sections; controls on the left, and a graph on the right.
        # The left side will consist of self.tabs for different types of controls, with the self.tabs implemented by QTabWidget.

        # Add a layout for the left side of the window
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabShape(QTabWidget.TabShape.Rounded)

        layout_left_tab1 = QVBoxLayout()

        # Create a frame around the position input fields.
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(2)

        widget = QWidget()
        position_layout = QVBoxLayout()
        # Add a label for this box.
        label = QLabel("Position")
        # Center the label horizontally and align it to the top.
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        position_layout.addWidget(label)
        # Add a label and two input fields for the start position.
        layout = QHBoxLayout()
        label = QLabel("Start:")
        self.position_label_start_x = QLineEdit()
        self.position_label_start_y = QLineEdit()
        self.position_label_start_x.returnPressed.connect(lambda: self.update_position())
        self.position_label_start_y.returnPressed.connect(lambda: self.update_position())
        layout.addWidget(label)
        layout.addWidget(self.position_label_start_x)
        layout.addWidget(self.position_label_start_y)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        position_layout.addLayout(layout)
        # Add a label and two input fields for the end position.
        layout = QHBoxLayout()
        label = QLabel("End:")
        self.position_label_end_x = QLineEdit()
        self.position_label_end_y = QLineEdit()
        self.position_label_end_x.returnPressed.connect(lambda: self.update_position())
        self.position_label_end_y.returnPressed.connect(lambda: self.update_position())
        layout.addWidget(label)
        layout.addWidget(self.position_label_end_x)
        layout.addWidget(self.position_label_end_y)
        position_layout.addLayout(layout)
        # Add an apply and reset button.
        layout = QHBoxLayout()
        button = QPushButton("Apply")
        button.clicked.connect(lambda: self.update_position())
        layout.addWidget(button)
        button = QPushButton("Reset")
        button.clicked.connect(lambda: self.update_position('reset'))
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        position_layout.addLayout(layout)
        position_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget.setLayout(position_layout)
        frame.setLayout(position_layout)
        layout_left_tab1.addWidget(frame)
        self.position_frame = frame
        self.position_frame.setFixedHeight(int(self.tabs.height() * 0.5))

        widget = QCheckBox()
        widget.setCheckState(Qt.CheckState.Checked)
        widget.stateChanged.connect(self.show_state)
        layout_left_tab1.addWidget(widget)

        widget = QPushButton("Click me")
        widget.clicked.connect(self.open_dialog)
        layout_left_tab1.addWidget(widget)

        layout = QHBoxLayout()
        # Add a save button that opens a save dialog.
        widget = QPushButton("Save")
        widget.clicked.connect(self.save_file)
        layout.addWidget(widget)
        # Add a load button that opens a load dialog.
        widget = QPushButton("Load")
        widget.clicked.connect(self.load_file)
        layout.addWidget(widget)
        layout_left_tab1.addLayout(layout)

        widget_left_tab1 = QWidget()
        widget_left_tab1.setLayout(layout_left_tab1)
        self.tabs.addTab(widget_left_tab1, "Tab 1")

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
        self.tabs.addTab(widget_left_tab2, "Tab 2")

        # Set properties of the layout on the left side of the window.
        self.tabs.setMinimumSize(400, 300)
        self.tabs.setMaximumSize(800, 600)
        self.tabs.setAutoFillBackground(True)
        palette = self.tabs.palette()
        color = (100, 20, 20)
        palette.setColor(QPalette.ColorRole.Window, QColor(*color))
        self.tabs.setPalette(palette)

        # Add a layout that can be used to display a graph on the right side of the window.
        self.layout_right = QVBoxLayout()
        getLayoutMargins = self.layout_right.getContentsMargins
        self.graph = PlotWidget(parent=self, getLayoutMargins=getLayoutMargins)
        self.layout_right.addWidget(self.graph)
        color = QColor(50, 50, 50)
        self.graph.setBackground(color)
        self.graph.update_graph()

        # Set properties of the layout on the right side of the window.
        widget_right = QWidget()
        widget_right.setLayout(self.layout_right)
        widget_right.setMinimumSize(400, 300)
        widget_right.setMaximumSize(800, 600)
        widget_right.setStyleSheet("background-color: rgb(20, 100, 20)")
        widget_right.setMouseTracking(True)

        # Add the left and right layouts to the main layout of the window.
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.tabs)
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
        # self.resizeEvent(QResizeEvent(QSize(1000, 600), self.size()))

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        " Create a custom context menu. "
        plot_widget_rect = self.graph.geometry()
        plot_widget_rect.moveTopLeft(self.graph.mapTo(self, plot_widget_rect.topLeft()))
        if plot_widget_rect.contains(event.pos()):
            self.graph.contextMenuEvent(event)
            event.ignore()
        else:
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

    def load_file(self):
        " Open a load dialog. "
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "data", "Pickle (*.pkl)")
        if file_name:
            try:
                with open(file_name, 'rb') as file:
                    self.graph.x_data, self.graph.y_data = pickle.load(file)
                    print(f"File loaded from: {file_name}")
                    self.graph.reload()
            except Exception as e:
                print(f"Error: {e}")

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

    def resizeRefresh(self):
        self.resizeEvent(QResizeEvent(self.size(), self.size()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_height = int(self.tabs.height() * 0.25)
        self.position_frame.setFixedHeight(new_height)

    def save_file(self):
        " Open a save dialog. "
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "data/trajectory.pkl", "Pickle (.pkl)")
        if file_name:
            try:
                with open(file_name, 'wb') as file:
                    pickle.dump([self.graph.x_data, self.graph.y_data], file, pickle.HIGHEST_PROTOCOL)
                    print(f"File saved to: {file_name}")
            except Exception as e:
                print(f"Error: {e}")

    def show_state(self, state):
        " Print the state of the checkbox. "
        print(f"Checkbox state: {state}")

    def update_position(self, flag=None):
        " Update the position of the start and end points. "
        if flag == 'reset':
            self.position_label_start_x.setText(str(self.init_position[0][0]))
            self.position_label_start_y.setText(str(self.init_position[0][1]))
            self.position_label_end_x.setText(str(self.init_position[1][0]))
            self.position_label_end_y.setText(str(self.init_position[1][1]))
        self.graph.update_graph()

    def update_position_label(self, start, end):
        " Update the displayed text of the position input fields. "
        self.position_label_start_x.setText(str(start[0]))
        self.position_label_start_y.setText(str(start[1]))
        self.position_label_end_x.setText(str(end[0]))
        self.position_label_end_y.setText(str(end[1]))


if __name__ == "__main__":
    # Create an application. This contains the main event loop; it is required to run any PyQt program.
    app = QApplication(sys.argv)
    # Create a window. The parent of the window is None.
    window = MainWindow()
    # A window without a parent is not displayed. The window is displayed by calling the show() method.
    window.show()
    window.resizeRefresh()
    # Call the QApplication.exec() method to start the event loop.
    app.exec()
