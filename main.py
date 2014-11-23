#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QApplication


if __name__ == "__main__":
    import edistor
    import sys

    app = QApplication([])
    editor = edistor.Edistor()
    editor.setWindowTitle(editor.tr("Edistor"))
    editor.highlightCurrentLine('red', 30)
    editor.setMinimumSize(700, 500)
    editor.show()

    sys.exit(app.exec_())