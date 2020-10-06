import base64
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from variables import widgetMargins


tabDescription = "Convertisseur Base64"

class TabWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.groupBox1String = QLineEdit()
    self.groupBox1String.textChanged.connect(self.StringToBase64)
    self.groupBox1Result = QTextEdit()
    self.groupBox2Base64 = QTextEdit()
    self.groupBox2Base64.textChanged.connect(self.Base64ToString)
    self.groupBox2Result = QLineEdit()
    self.groupBox3Result = QTextEdit()
    self.groupBox4Base64 = QTextEdit()

    self.groupBox1Layout = QGridLayout()
    self.groupBox1Layout.addWidget(QLabel("Chaîne:"), 0, 0)
    self.groupBox1Layout.addWidget(self.groupBox1String, 0, 1)
    self.groupBox1Layout.addWidget(QLabel("Resultat:"), 1, 0)
    self.groupBox1Layout.addWidget(self.groupBox1Result, 1, 1)
    self.groupBox1 = QGroupBox("Chaîne => Base64")
    self.groupBox1.setLayout(self.groupBox1Layout)

    self.groupBox2Layout = QGridLayout()
    self.groupBox2Layout.addWidget(QLabel("Base64:"), 0, 0)
    self.groupBox2Layout.addWidget(self.groupBox2Base64, 0, 1)
    self.groupBox2Layout.addWidget(QLabel("Resultat:"), 1, 0)
    self.groupBox2Layout.addWidget(self.groupBox2Result, 1, 1)
    self.groupBox2 = QGroupBox("Base64 => Chaîne")
    self.groupBox2.setLayout(self.groupBox2Layout)

    self.groupBox3Layout = QGridLayout()
    self.groupBox3Layout.addWidget(QLabel("Fichier:"), 0, 0)
    self.groupBox3Layout.addWidget(self.OpenFileButton(), 0, 1)
    self.groupBox3Layout.addWidget(QLabel("Resultat:"), 1, 0)
    self.groupBox3Layout.addWidget(self.groupBox3Result, 1, 1)
    self.groupBox3 = QGroupBox("Fichier => Base64")
    self.groupBox3.setLayout(self.groupBox3Layout)

    self.groupBox4Layout = QGridLayout()
    self.groupBox4Layout.addWidget(QLabel("Base64:"), 0, 0)
    self.groupBox4Layout.addWidget(self.groupBox4Base64, 0, 1)
    self.groupBox4Layout.addWidget(QLabel("Resultat:"), 1, 0)
    self.groupBox4Layout.addWidget(self.SaveFileButton(), 1, 1)
    self.groupBox4 = QGroupBox("Base64 => Fichier")
    self.groupBox4.setLayout(self.groupBox4Layout)

    mainLayout = QGridLayout()
    mainLayout.setContentsMargins(widgetMargins)
    mainLayout.setAlignment(Qt.AlignTop)
    mainLayout.addWidget(self.groupBox1, 1, 0)
    mainLayout.addWidget(self.groupBox2, 1, 1)
    mainLayout.addWidget(self.groupBox3, 2, 0)
    mainLayout.addWidget(self.groupBox4, 2, 1)
    self.setLayout(mainLayout)


  def StringToBase64(self):
    try:
      self.groupBox1Result.setText(base64.encodebytes(self.groupBox1String.text().encode('utf-8')).decode('utf-8'))
    except Exception:
      self.groupBox1Result.setText("")


  def Base64ToString(self):
    try:    
      self.groupBox2Result.setText(base64.decodebytes(self.groupBox2Base64.toPlainText().encode('utf-8')).decode('utf-8'))
    except Exception:
      self.groupBox2Result.setText("")


  def OpenFileButton(self):
    def Callback(button, path):
      import os, io
      if os.path.exists(path):
        button.setText("...%s" % path[-30:])
        with io.open(file=path, mode="rb") as file:
          buffer = file.read()
          self.groupBox3Result.setText(base64.b64encode(buffer).decode('utf-8'))

    button = QPushButton()
    button.setText("...")
    button.clicked.connect(lambda: Callback(button, QFileDialog().getOpenFileName()[0]))
    return button
  

  def SaveFileButton(self):
    def Callback(button, path):
      import io
      button.setText(f"...{path[-30:]}")
      with io.open(path, "xb") as file:
        buffer = base64.b64decode(self.groupBox4Base64.toPlainText().encode('utf-8'))
        file.write(buffer)

    button = QPushButton()
    button.setText("...")
    button.clicked.connect(lambda: Callback(button, QFileDialog().getSaveFileName()[0]))
    return button

