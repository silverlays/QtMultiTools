import images
import sys

from PySide6.QtCore import *
from PySide6.QtGui import QFont, QCursor, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QSpacerItem, QCommandLinkButton, QVBoxLayout, QGridLayout, QGroupBox

from importlib import import_module
from QtDarkTheme import QtDarkTheme
from variables import tabsList, TextShadow
from mainwindow_ui import Ui_MainWindow


buildVersion = "0.7 (Alpha)"


class App(QMainWindow, Ui_MainWindow, QObject):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.retranslateUi(self)

    ### WINDOW SETUP
    self.setWindowTitle(f"{self.windowTitle()} v{buildVersion}")

    ### TABS SETUP
    for tabDescription, tabTarget in tabsList.items():
      module = import_module(f"tabs.{tabTarget}")
      self.tabWidget.addTab(module.TabWidget(), tabDescription)
      
      if hasattr(module, "options"):
        menuOptions = self.menuOptions.addMenu(tabDescription)
        for option in module.options:
          menuOptions.addAction(option)

    self.tabWidget.addTab(self.AboutTab(), "A propos de moi...")

    ### STATUS BAR
    self.statusbar.showMessage(f"Modules chargés: {self.tabWidget.count()}")
    resetButton = QPushButton()
    resetButton.setIcon(images.GetResetIcon())
    resetButton.clicked.connect(self.Reset)
    self.statusbar.addPermanentWidget(resetButton)


  def AboutTab(self):
    import webbrowser
    programLabel = QLabel(f"Silv3r's MultiTools v{buildVersion}")
    programLabel.setStyleSheet("color: #aaffff; font-size: 36px")
    programLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    programLabel.setGraphicsEffect(TextShadow())

    spacer = QSpacerItem(0, 25)

    descriptionLabel = QLabel("Programme créé par et pour Silv3r regroupant tous les outils nécessaires pour faciliter la programmation, la maintenance et et pleins d'autres choses :)")
    descriptionLabel.setStyleSheet("font-size: 14px; font-style: italic")
    descriptionLabel.setGraphicsEffect(TextShadow())
    descriptionLabel.setWordWrap(True)

    twitchLink = QCommandLinkButton("https://www.twitch.tv/silv3r_ow", "Ma chaîne Twitch")
    twitchLink.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    twitchLink.clicked.connect(lambda: webbrowser.open(twitchLink.text()))

    youtubeLink = QCommandLinkButton("https://www.youtube.com/channel/UC9pLDlEx1XI0WNo-K23aH7A", "Ma chaîne YouTube")
    youtubeLink.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    youtubeLink.clicked.connect(lambda: webbrowser.open(youtubeLink.text()))

    linksGroupBoxLayout = QGridLayout()
    linksGroupBoxLayout.addWidget(twitchLink)
    linksGroupBoxLayout.addWidget(youtubeLink)

    linksGroupBox = QGroupBox("Liste de liens pouvant être utile :")
    linksGroupBox.setLayout(linksGroupBoxLayout)

    layout = QVBoxLayout()
    layout.setContentsMargins(100, 20, 100, 20)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.addWidget(programLabel)
    layout.addSpacerItem(spacer)
    layout.addWidget(descriptionLabel)
    layout.addSpacerItem(spacer)
    layout.addWidget(linksGroupBox)

    widget = QWidget()
    widget.setLayout(layout)
    return widget

  def Reset(self):
    import os, subprocess
    self.close()
    subprocess.call(["py", os.path.abspath(__file__)])
  
  def SaveConfig(self):
    ### TODO ###
    print("--- TODO ---")


if __name__ == "__main__":
  app = QApplication(sys.argv) # /!\ MUST BE HERE /!\

  font = QFont()
  font.setFamily(app.font().family())
  font.setPointSize(10)
  font.setWeight(QFont.Weight.Bold)

  app.setWindowIcon(images.GetAppIcon())
  app.setStyle("Fusion")
  app.setFont(font)
  app.setPalette(QtDarkTheme())

  myApp = App()
  myApp.show()
  sys.exit(app.exec())