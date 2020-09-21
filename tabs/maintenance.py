from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from variables import widgetMargins


class Maintenance(QWidget):
  buttonsFixedWidth = 500
  buttonsFixedHeight = 40

  def __init__(self):
    super().__init__()

    groupBoxLayout = QVBoxLayout()
    groupBoxLayout.addWidget(self.ClearCacheButton())

    mainGroupBox = QGroupBox("Fonctions disponibles pour la maintenance du PC")
    mainGroupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
    mainGroupBox.setLayout(groupBoxLayout)

    mainLayout = QVBoxLayout()
    mainLayout.setContentsMargins(widgetMargins)
    mainLayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
    mainLayout.addWidget(mainGroupBox)

    self.setLayout(mainLayout)
  
  
  def ClearCacheButton(self):
    button = QPushButton("Effacer le cache des icônes du système")
    button.setFixedHeight(self.buttonsFixedHeight)
    button.clicked.connect(lambda: QMessageBox.warning(self, "TODO", "En construction..."))
    return button