from PyQt6.QtCore import QMargins
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

widgetMargins = QMargins(200, 20, 200, 20)

def TextShadow():
  textShadow = QGraphicsDropShadowEffect()
  textShadow.setColor(QColor(32, 32, 32))
  textShadow.setOffset(5, 5)
  textShadow.setBlurRadius(8)
  return textShadow

