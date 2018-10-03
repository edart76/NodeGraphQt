#!/usr/bin/python
from PySide2 import QtWidgets, QtCore, QtGui


class ColorSolid(QtWidgets.QWidget):

    def __init__(self, parent=None, color=None):
        super(ColorSolid, self).__init__(parent)
        self.setMinimumSize(15, 15)
        self.setMaximumSize(15, 15)
        self.color = color or (255, 0, 0, 255)
        self.setToolTip('rgba{}'.format(self.color))

    def paintEvent(self, event):
        size = self.geometry()
        rect = QtCore.QRect(1, 1, size.width() - 2, size.height() - 2)
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(*self.color))
        painter.drawRoundedRect(rect, 4, 4)


class ColorButton(QtWidgets.QWidget):

    color_submitted = QtCore.Signal(tuple)

    def __init__(self, parent=None, color=None):
        super(ColorButton, self).__init__(parent)
        self._solid = ColorSolid(self, color)
        self._solid.setMaximumHeight(15)
        button = QtWidgets.QPushButton('select color')
        button.clicked.connect(self._on_select_color)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(button)
        layout.addWidget(self._solid)

    def _on_select_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color = color.getRgb()
            self.color_submitted.emit(self.color)

    @property
    def color(self):
        return self._solid.color

    @color.setter
    def color(self, rgba=None):
        self._solid.color = rgba
        self._solid.setToolTip('rgba{}'.format(rgba))
        self.update()


class NodePropertyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, node=None):
        super(NodePropertyWidget, self).__init__(parent)
        self._node = node
        self.widgets = {
            'name': QtWidgets.QLineEdit(),
            'color': ColorButton(self),
            # 'border_color': ColorButton(self),
            'text_color': ColorButton(self),
            'disabled': QtWidgets.QCheckBox(self),
        }
        self.layout()
        default_layout = QtWidgets.QGridLayout(self)
        default_layout.setContentsMargins(4, 4, 4, 4)
        default_layout.setSpacing(4)
        default_layout.setColumnMinimumWidth(0, 100)
        default_layout.setColumnMinimumWidth(1, 100)
        x = 0
        for name, widget in self.widgets.items():
            label = QtWidgets.QLabel(name.replace('_', ' '))
            default_layout.addWidget(label, x, 0, 1, 1, QtCore.Qt.AlignRight)
            default_layout.addWidget(widget, x, 1)
            x += 1
        default_layout.addWidget(self._create_line(), x, 0, 1, 2)


    def _create_line(self):
        line = QtWidgets.QFrame(self)
        line.setFrameShape(line.HLine)
        line.setFrameShadow(line.Sunken)
        line.setMinimumHeight(10)
        return line

    def _create_prop_widgets(self):
        self._widgets['id'] = QtWidgets.QLabel()
        self._widgets['type'] = QtWidgets.QLabel()
        self._widgets['name'] = QtWidgets.QLabel()

    # def wire_signals(self):
    #     self.node.widgets

    @property
    def node(self):
        return self._node


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    button = NodePropertyWidget()
    button.show()

    app.exec_()
