from PySide6.QtCore import QMargins
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

tabsList = {
  "Suivi des séries": "suivi_series",
  "Convertisseur Base64": "base64",
  "Sélecteur de couleur": "colorpicker",
  "Maintenance du PC": "maintenance",
  "Résolutions par ratio d'aspect": "resolutions",
}

widgetMargins = QMargins(200, 20, 200, 20)

def TextShadow():
  textShadow = QGraphicsDropShadowEffect()
  textShadow.setColor(QColor(32, 32, 32))
  textShadow.setOffset(5, 5)
  textShadow.setBlurRadius(8)
  return textShadow

