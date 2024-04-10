from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from variables import widgetMargins


class TabWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.colorDialog = QColorDialog()

    self.colorDialogButton = QPushButton()
    self.colorDialogButton.clicked.connect(self.GetColor)
    self.colorDialogButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    self.hexEdit = QLineEdit()
    self.hexEdit.setEnabled(False)
    self.rgbEdit = QLineEdit()
    self.rgbEdit.setEnabled(False)
    self.sampleTextLight = QLabel("Ceci est un exemple de texte sur fond clair")
    self.sampleTextLight.setStyleSheet("padding: 10px; background-color: white; color: black")
    self.sampleTextDark = QLabel("Ceci est un exemple de texte sur fond foncé")
    self.sampleTextDark.setStyleSheet("padding: 10px; background-color: black; color: white")

    self.groupBoxLayout = QGridLayout()
    self.groupBoxLayout.setVerticalSpacing(5)
    self.groupBoxLayout.addWidget(self.colorDialogButton, 0, 0, 2, 1)
    self.groupBoxLayout.addWidget(QLabel("Hex:"), 0, 1)
    self.groupBoxLayout.addWidget(self.hexEdit, 0, 2)
    self.groupBoxLayout.addWidget(self.ClipboardButton(self.hexEdit), 0, 3)
    self.groupBoxLayout.addWidget(QLabel("RGB:"), 1, 1)
    self.groupBoxLayout.addWidget(self.rgbEdit, 1, 2)
    self.groupBoxLayout.addWidget(self.ClipboardButton(self.rgbEdit), 1, 3)
    self.groupBoxLayout.addItem(QSpacerItem(0, 15), 2, 0)
    self.groupBoxLayout.addWidget(self.sampleTextLight, 3, 0, 1, 4)
    self.groupBoxLayout.addWidget(self.sampleTextDark, 4, 0, 1, 4)
    self.groupBoxLayout.setColumnStretch(2, 3)
    
    self.groupBox = QGroupBox("Cliquez sur le bouton pour sélectionner une couleur")
    self.groupBox.setLayout(self.groupBoxLayout)

    mainLayout = QGridLayout()
    mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    mainLayout.setContentsMargins(widgetMargins)
    mainLayout.addWidget(self.groupBox, 1, 0)
    self.setLayout(mainLayout)

  def ClipboardButton(self, referTo):
    import pyperclip as clipboard
    button = QPushButton()
    button.setText("C")
    button.setMaximumWidth(25)
    button.clicked.connect(lambda: clipboard.copy(referTo.text()))
    return button
  
  def GetColor(self):
    color = QColor(self.colorDialog.getColor())
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(0,0,0))
    palette.setColor(QPalette.ColorRole.Button, color)
    self.colorDialogButton.setPalette(palette)
    self.hexEdit.setText(color.name())
    self.rgbEdit.setText(str.format(f"rgb({color.red()}, {color.green()}, {color.blue()})"))
    self.sampleTextLight.setStyleSheet(f"padding: 10px; background-color: white; color: {color.name()}")
    self.sampleTextDark.setStyleSheet(f"padding: 10px; background-color: black; color: {color.name()}")