from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

widgetMargins = QMargins(200, 20, 200, 20)

def TextShadow():
  textShadow = QGraphicsDropShadowEffect()
  textShadow.setColor(QColor(32, 32, 32))
  textShadow.setOffset(5, 5)
  textShadow.setBlurRadius(8)
  return textShadow

