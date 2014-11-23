# -*- coding: utf-8 -*-
# This file is part of Edistor

# Sidebar line number area for Edistor
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QPainter,
    QPalette
    )

from PyQt4.QtCore import (
    Qt,
    )


class Sidebar(QWidget):

    LEFT_MARGIN = 6
    RIGHT_MARGIN = 6

    def __init__(self, edistor):
        QWidget.__init__(self, edistor)
        self._edistor = edistor

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.fillRect(e.rect(), self.palette().color(QPalette.Window))
        qp.setPen(Qt.black)

        block = self._edistor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self._edistor.blockBoundingGeometry(block).translated(
                  self._edistor.contentOffset()).top())
        bottom = top + int(self._edistor.blockBoundingRect(block).height())

        while block.isValid() and top <= e.rect().bottom():
            if block.isVisible() and bottom >= e.rect().top():
                number = str(block_number + 1)
                qp.drawText(0, top, self.width(),
                            self._edistor.fontMetrics().height(),
                            Qt.AlignRight, number)
            block = block.next()
            boundingRect = self._edistor.blockBoundingRect(block)
            top = bottom
            bottom = top + int(boundingRect.height())
            block_number += 1

    def width(self):
        digits = len(str(max(1, self._edistor.blockCount())))
        return Sidebar.LEFT_MARGIN + self._edistor.fontMetrics().width('9') * \
                digits + Sidebar.RIGHT_MARGIN