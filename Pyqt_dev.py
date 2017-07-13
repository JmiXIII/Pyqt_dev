# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:48:11 2017

@author: user11
"""

from PyQt5.QtCore import QDir, Qt, QRect, QSize
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy, QRubberBand)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter


class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.imageLabel = QLabel()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                              triggered=self.open)
        self.fitAct = QAction("&Resize...", self, shortcut="Ctrl+F",
                              triggered=self.fit)
        self.ogSizeAct = QAction("&Original size ...",self,shortcut="ctrl+G",
                              triggered=self.ogSize)
        self.ocrAct = QAction("&OCR...", self, shortcut="Ctrl+O",
                              triggered=self.ocr)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)

        self.editMenu = QMenu("&Edit", self)
        self.editMenu.addAction(self.fitAct)
        self.editMenu.addAction(self.ogSizeAct)
        self.editMenu.addAction(self.ocrAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.editMenu)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                QDir.currentPath())
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            self.pixmap = QPixmap.fromImage(image)
            self.imageLabel.setPixmap(self.pixmap)
            self.imageLabel.adjustSize()
            # self.scaleFactor = 1.0

    def fit(self):
        repixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(repixmap)
        self.imageLabel.adjustSize()

    def ogSize(self):
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.adjustSize()

    def ocr(self):
        self.pixmap.save("test",'jpg')
        pass

    def mousePressEvent (self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        cropPixmap = self.pixmap.copy(currentQRect)
        cropPixmap.save("temp.jpg",'jpg')
#        self.imageLabel.setPixmap(cropPixmap)
#        self.imageLabel.adjustSize()
#        cropPixmap.save("temp.jpg",'jpg')

#import sys
#from PyQt4 import QtGui, QtCore
#
#class QExampleLabel (QtGui.QLabel):
#    def __init__(self, parentQWidget = None):
#        super(QExampleLabel, self).__init__(parentQWidget)
#        self.initUI()
#
#    def initUI (self):
#        self.setPixmap(QtGui.QPixmap('input.png'))
#
#    def mousePressEvent (self, eventQMouseEvent):
#        self.originQPoint = eventQMouseEvent.pos()
#        self.currentQRubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self)
#        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
#        self.currentQRubberBand.show()
#
#    def mouseMoveEvent (self, eventQMouseEvent):
#        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())
#
#    def mouseReleaseEvent (self, eventQMouseEvent):
#        self.currentQRubberBand.hide()
#        currentQRect = self.currentQRubberBand.geometry()
#        self.currentQRubberBand.deleteLater()
#        cropQPixmap = self.pixmap().copy(currentQRect)
#        cropQPixmap.save('output.png')
#
#if __name__ == '__main__':
#    myQApplication = QtGui.QApplication(sys.argv)
#    myQExampleLabel = QExampleLabel()
#    myQExampleLabel.show()
#    sys.exit(myQApplication.exec_())

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    app.exec_()
