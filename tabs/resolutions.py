from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from variables import widgetMargins, TextShadow


class Resolutions(QWidget):
  def __init__(self):
    super().__init__()
    
    self.aspectComboBox = QComboBox()
    self.aspectComboBox.addItem("4:3")
    self.aspectComboBox.addItem("16:9")
    self.aspectComboBox.addItem("16:10")
    self.aspectComboBox.addItem("21:9")
    self.aspectComboBox.currentIndexChanged.connect(self.ChangeResolution)
    
    self.resolutionsGroupBoxStackedLayout = QStackedLayout()
    self.CreateResolutions()
    self.resolutionsGroupBox = QGroupBox("Liste des résolutions (divisible par 8)")
    self.resolutionsGroupBox.setLayout(self.resolutionsGroupBoxStackedLayout)

    mainlayout = QFormLayout()
    mainlayout.setAlignment(Qt.AlignTop)
    mainlayout.setContentsMargins(widgetMargins)
    mainlayout.addRow(QLabel("Ratio d'aspect:"), self.aspectComboBox)
    mainlayout.setSpacing(20)
    mainlayout.addRow(self.resolutionsGroupBox)

    self.setLayout(mainlayout)


  def CreateResolutions(self):
    for resolutionIndex in range(self.aspectComboBox.count()):
      widget = QWidget()
      layout = QGridLayout()

      [aspectX, aspectY] = self.aspectComboBox.itemText(resolutionIndex).split(":")
      aspectX = int(aspectX)
      aspectY = int(aspectY)
      x, y = 1, 1

      for column in range(0, 5):
        for row in range(0, 15):
          while (x * aspectX) % 8 != 0 or (y * aspectY) % 8 != 0:
            x +=1
            y += 1
          resLabel = QLabel("%sx%s" % (x * aspectX, y * aspectY))
          resLabel.setAlignment(Qt.AlignCenter)
          resLabel.setGraphicsEffect(TextShadow())
          layout.addWidget(resLabel, row, column)
          x += 1
          y += 1          

      widget.setLayout(layout)
      self.resolutionsGroupBoxStackedLayout.addWidget(widget)
  
  
  def ChangeResolution(self):
    import random
    self.resolutionsGroupBoxStackedLayout.setCurrentIndex(self.aspectComboBox.currentIndex())