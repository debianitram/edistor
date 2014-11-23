# -*- coding: utf-8 -*-

# Edistor: editor for EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QPlainTextEdit,
    QPainter,
    QFontMetricsF,
    QColor,
    QTextEdit,
    QTextFormat,
    )

from PyQt4.QtCore import (
    QVariant,
    QRect,
    SIGNAL
    )

from sidebar import Sidebar


class Edistor(QPlainTextEdit):
    """ QPlainTextEdit implementation

        This class is the base of editor

        Highlight current line method:
            @color: string color
            @alpha: int
    """

    def __init__(self):
        QPlainTextEdit.__init__(self)
        self.position_margin = QFontMetricsF(
            self.document().defaultFont()).width("#") * 80
        # Margin line
        self._margin = None
        # Sidebar
        self.sidebar = Sidebar(self)
        # Highlight current line
        self._color_current_line = QColor('lightblue')
        self._alpha_current_line = self._color_current_line.setAlpha(50)
        self._highlight_current_line()
        # Connection
        self.connect(self, SIGNAL("blockCountChanged(int)"),
                    self._update_sidebar_area_width)
        self.connect(self, SIGNAL("updateRequest(QRect, int)"),
                    self._update_sidebar_areas)
        self.connect(self, SIGNAL("cursorPositionChanged()"),
                    self._highlight_current_line)

    def margin(self, show=False):
        """ Margin line default desactivate """

        self._margin = show
        self._margin_color = QColor('blue')
        self._margin_alpha = 60

    def margin_color(self, color):
        """ Set the color of margin line """

        self._margin_color = QColor(color)

    def margin_alpha(self, alpha):
        """ Set the alpha of margin line """

        self._margin_alpha = alpha

    def paintEvent(self, e):
        QPlainTextEdit.paintEvent(self, e)
        if self._margin:
            qp = QPainter()
            qp.begin(self.viewport())
            qp.setPen(self._margin_color)
            offset = self.contentOffset()
            background = self._margin_color
            background.setAlpha(self._margin_alpha)
            qp.drawLine(self.position_margin + offset.x(), 0,
                        self.position_margin + offset.x(),
                        self.viewport().height())
            qp.end()

    def highlightCurrentLine(self, color, alpha):
        self._color_current_line = QColor(color)
        self._alpha_current_line = self._color_current_line.setAlpha(alpha)
        self._highlight_current_line()

    def _highlight_current_line(self):
        self.extra_selections = []
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(self._color_current_line)
        selection.format.setProperty(
            QTextFormat.FullWidthSelection, QVariant(True))
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.extra_selections.append(selection)
        self.setExtraSelections(self.extra_selections)

    def _update_sidebar_area_width(self, new_block_count):
        self.setViewportMargins(self.sidebar.width(), 0, 0, 0)

    def _update_sidebar_areas(self, rect, dy):
        if dy:
            self.sidebar.scroll(0, dy)
        else:
            self.sidebar.update(0, rect.y(), self.sidebar.width(),
                                rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_sidebar_area_width(0)

    def resizeEvent(self, e):
        QPlainTextEdit.resizeEvent(self, e)
        cr = self.contentsRect()
        self.sidebar.setGeometry(QRect(cr.left(), cr.top(),
                                self.sidebar.width(), cr.height()))
