from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from variables import widgetMargins


class TabWidget(QWidget):
  buttonsFixedWidth = 500
  buttonsFixedHeight = 40

  def __init__(self):
    super().__init__()

    groupBoxLayout = QVBoxLayout()
    groupBoxLayout.addWidget(self.ClearCacheButton())

    mainGroupBox = QGroupBox("Fonctions disponibles pour la maintenance du PC")
    mainGroupBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    mainGroupBox.setLayout(groupBoxLayout)

    mainLayout = QVBoxLayout()
    mainLayout.setContentsMargins(widgetMargins)
    mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
    mainLayout.addWidget(mainGroupBox)

    self.setLayout(mainLayout)
    
  def ClearCacheButton(self) -> QPushButton:
    button = QPushButton("Effacer le cache des icônes du système")
    button.setFixedHeight(self.buttonsFixedHeight)
    button.clicked.connect(lambda: QMessageBox.warning(self, "TODO", "En construction..."))
    return button