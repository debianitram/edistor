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
        self._bold = False

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.fillRect(e.rect(), self.palette().color(QPalette.Window))
        qp.setPen(Qt.black)

        block = self._edistor.firstVisibleBlock()
        block_number = block.blockNumber()
        text_cursor_position = self._edistor.textCursor().position()
        actual_block = self._edistor.document().findBlock(text_cursor_position)
        top = int(self._edistor.blockBoundingGeometry(block).translated(
                  self._edistor.contentOffset()).top())
        bottom = top + int(self._edistor.blockBoundingRect(block).height())

        while block.isValid() and top <= e.rect().bottom():
            # Set bold current line
            if block == actual_block:
                self._bold = True
                font = qp.font()
                font.setBold(True)
                qp.setFont(font)

            if block.isVisible() and bottom >= e.rect().top():
                number = str(block_number + 1)
                qp.drawText(0, top, self.width(),
                            self._edistor.fontMetrics().height(),
                            Qt.AlignRight, number)

            if self._bold:
                font = qp.font()
                font.setBold(False)
                qp.setFont(font)

            block = block.next()
            boundingRect = self._edistor.blockBoundingRect(block)
            top = bottom
            bottom = top + int(boundingRect.height())
            block_number += 1

    def width_(self):
        digits = len(str(max(1, self._edistor.blockCount())))
        ancho = Sidebar.LEFT_MARGIN + self._edistor.fontMetrics().width('0') * \
                digits + Sidebar.RIGHT_MARGIN
        if self.width() != ancho:
            self.setFixedWidth(ancho)
            self._edistor.setViewportMargins(ancho, 0, 0, 0)
        return ancho