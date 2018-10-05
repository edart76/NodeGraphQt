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

    color_selected = QtCore.Signal(tuple)

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
            self.color_selected.emit(self.color)

    @property
    def color(self):
        return self._solid.color

    @color.setter
    def color(self, rgba=None):
        self._solid.color = rgba
        self._solid.setToolTip('rgba{}'.format(rgba))
        self.update()


class NodePropertyWidget(QtWidgets.QWidget):

    property_changed = QtCore.Signal(str, object)

    def __init__(self, parent=None, node=None):
        """
        Args:
            parent (NodeGraphQt.widgets.viewer.NodeViewer): node graph widget.
            node (NodeGraphQt.Node): node instance.
        """
        super(NodePropertyWidget, self).__init__(parent)
        title = '({}) '.format(node.name()) if node else ''
        title += 'node properties'
        self.setWindowTitle(title)
        self._node = node
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(1, 1, 1, 1)

        # setup node default property widgets.
        self.widgets = {
            'name': QtWidgets.QLineEdit(),
            'color': ColorButton(self),
            # 'border_color': ColorButton(self),
            'text_color': ColorButton(self),
            'disabled': QtWidgets.QCheckBox(self),
        }
        prop_layout = QtWidgets.QGridLayout()
        prop_layout.setContentsMargins(4, 4, 4, 4)
        prop_layout.setSpacing(2)
        prop_layout.setColumnMinimumWidth(0, 80)
        prop_layout.setColumnMinimumWidth(1, 100)
        x = 0
        for name, widget in self.widgets.items():
            label = QtWidgets.QLabel(name.replace('_', ' '))
            prop_layout.addWidget(label, x, 0, 1, 1, QtCore.Qt.AlignRight)
            prop_layout.addWidget(widget, x, 1)
            x += 1
        self._layout.addLayout(prop_layout)
        self._layout.addWidget(self.__divider())

        # wire up default node property widgets.
        for name, widget in self.widgets.items():
            self.__wire_widget(name, widget)

        # setup custom properties.
        self.custom_widgets = {}
        for prop in self.node.properties()


        # wireup the node widgets.
        if hasattr(self.node, 'widgets'):
            for name, widget in self.node.widgets().items():
                self.__wire_node_widgets(name, widget)



    def __wire_widget(self, name, widget):
        if isinstance(widget, ColorButton):
            widget.color_selected.connect(
                lambda value, prop=name: self.__on_prop_changed(prop, value))
        elif isinstance(widget, QtWidgets.QCheckBox):
            widget.stateChanged.connect(
                lambda value, prop=name: self.__on_prop_changed(prop, value == 2))
        elif isinstance(widget, QtWidgets.QLineEdit):
            widget.returnPressed.connect(
                lambda value, prop=name: self.__on_prop_changed(prop, value))

    def __wire_node_widgets(self, widget):
        return


    def __on_prop_changed(self, name, value):
        print(name, value)

    def __divider(self):
        line = QtWidgets.QFrame(self)
        line.setFrameShape(line.HLine)
        line.setFrameShadow(line.Sunken)
        line.setMinimumHeight(10)
        return line

    def __build_widgets(self):
        self._widgets['id'] = QtWidgets.QLabel()
        self._widgets['type'] = QtWidgets.QLabel()
        self._widgets['name'] = QtWidgets.QLabel()

    @property
    def node(self):
        return self._node


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    button = NodePropertyWidget()
    button.show()

    app.exec_()
