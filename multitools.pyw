import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from QtDarkTheme import QtDarkTheme
from variables import TextShadow

app = QApplication(sys.argv) # /!\ MUST BE HERE /!\

buildVersion = "0.5 (Alpha)"


class MainWindow(QMainWindow):
  ### Add import...
  from tabs.colorpicker import ColorPicker
  from tabs.base64 import Base64
  from tabs.maintenance import Maintenance
  from tabs.resolutions import Resolutions
  from tabs.suivi_series import SuiviSeries

  ### ...and insert an entry {"Tab text": ClassName()} for each component
  tabsList = {
    "Sélecteur de couleur": ColorPicker(),
    "Convertisseur Base64": Base64(),
    "Maintenance du PC": Maintenance(),
    "Résolutions par ratio d'aspect": Resolutions(),
    "Suivi des séries": SuiviSeries(),
  }


  def __init__(self):
    super().__init__()

    ### STATUS BAR
    self.statusBar = QStatusBar()
    self.statusBar.showMessage("Modules chargés: %s" % self.tabsList.__len__())
    resetButton = QPushButton()
    resetButton.setIcon(QIcon("images/reset.png"))
    resetButton.clicked.connect(self.Reset)
    self.statusBar.addPermanentWidget(resetButton)

    ### CENTRAL WIDGET
    self.tabsContainer = QTabWidget()
    self.tabsList = dict(sorted(self.tabsList.items(), key=lambda item: item[0])) # SORT TABS ALPHABETICALY
    for tab in self.tabsList: self.tabsContainer.addTab(self.tabsList[tab], tab)
    self.tabsContainer.addTab(self.AboutTab(), "A propos...")
    
    ### WINDOW'S PROPERTIES
    self.setWindowTitle("Silv3r's MultiTools v%s" % buildVersion)
    self.setMinimumSize(1280, 900)
    self.setCentralWidget(self.tabsContainer)
    self.setStatusBar(self.statusBar)
    self.show()
  
  def AboutTab(self):
    import webbrowser
    programLabel = QLabel("Silv3r's MultiTools v%s" % buildVersion)
    programLabel.setStyleSheet("color: #aaffff; font-size: 36px")
    programLabel.setAlignment(Qt.AlignCenter)
    programLabel.setGraphicsEffect(TextShadow())

    spacer = QSpacerItem(0, 25)

    descriptionLabel = QLabel("Programme créé par et pour Silv3r regroupant tous les outils nécessaires pour faciliter la programmation, la maintenance et et pleins d'autres choses :)")
    descriptionLabel.setStyleSheet("font-size: 14px; font-style: italic")
    descriptionLabel.setGraphicsEffect(TextShadow())
    descriptionLabel.setWordWrap(True)

    twitchLink = QCommandLinkButton("https://www.twitch.tv/silv3r_ow", "Ma chaîne Twitch")
    twitchLink.setCursor(QCursor(Qt.PointingHandCursor))
    twitchLink.clicked.connect(lambda: webbrowser.open(twitchLink.text()))

    youtubeLink = QCommandLinkButton("https://www.youtube.com/channel/UC9pLDlEx1XI0WNo-K23aH7A", "Ma chaîne YouTube")
    youtubeLink.setCursor(QCursor(Qt.PointingHandCursor))
    youtubeLink.clicked.connect(lambda: webbrowser.open(youtubeLink.text()))

    linksGroupBoxLayout = QGridLayout()
    linksGroupBoxLayout.addWidget(twitchLink)
    linksGroupBoxLayout.addWidget(youtubeLink)

    linksGroupBox = QGroupBox("Liste de liens pouvant être utile :")
    linksGroupBox.setLayout(linksGroupBoxLayout)

    layout = QVBoxLayout()
    layout.setContentsMargins(100, 20, 100, 20)
    layout.setAlignment(Qt.AlignTop)
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


if __name__ == "__main__":
  font = QFont()
  font.setFamily(app.font().family())
  font.setPointSize(10)
  font.setWeight(QFont.Bold)

  app.setWindowIcon(QIcon("images/app.ico"))
  app.setStyle("Fusion")
  app.setFont(font)
  app.setPalette(QtDarkTheme())

  mainwindow = MainWindow()
  sys.exit(app.exec_())