from os import error
import images, sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from QtDarkTheme import QtDarkTheme
from variables import TextShadow


app = QApplication(sys.argv) # /!\ MUST BE HERE /!\
buildVersion = "0.6 (Alpha)"


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.LoadModules()

    ### MENU BAR
    self.menuBar = QMenuBar()
    menuOptions = QMenu("Options", self.menuBar)
    menuOptions.addAction("Modifier les options", self.OptionsDialog)
    self.menuBar.addMenu(menuOptions)

    ### STATUS BAR
    self.statusBar = QStatusBar()
    self.statusBar.showMessage(f"Modules chargés: {self.tabsList.__len__()}")
    resetButton = QPushButton()
    resetButton.setIcon(images.GetResetIcon())
    resetButton.clicked.connect(self.Reset)
    self.statusBar.addPermanentWidget(resetButton)

    ### CENTRAL WIDGET
    self.tabsContainer = QTabWidget()
    # self.tabsList = dict(sorted(self.tabsList.items(), key=lambda item: item[0])) # SORT TABS ALPHABETICALY
    for tab in self.tabsList: self.tabsContainer.addTab(self.tabsList[tab], tab)
    self.tabsContainer.addTab(self.AboutTab(), "A propos...")
    
    ### WINDOW'S PROPERTIES
    self.setWindowTitle(f"Silv3r's MultiTools v{buildVersion}")
    self.setMinimumSize(1280, 900)
    self.setMenuBar(self.menuBar)
    self.setCentralWidget(self.tabsContainer)
    self.setStatusBar(self.statusBar)
    self.show()

  def LoadModules(self):
    import tabs

    self.tabsList = tabs.tabsList

  def OptionsDialog(self):
    dialog = QDialog(self, Qt.Dialog)
    dialog.setWindowTitle("Options")
    dialog.setModal(True)
    dialog.accepted.connect(self.SaveConfig)
    layout = QVBoxLayout(dialog)
    
    for tab in self.tabsList:
      checkbox = QCheckBox(tab)
      checkbox.setChecked(True)
      layout.addWidget(checkbox)
    
    dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    dialogButtons.accepted.connect(dialog.accept)
    dialogButtons.rejected.connect(dialog.reject)
    layout.addWidget(dialogButtons)

    dialog.setLayout(layout)
    dialog.show()

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
  font = QFont()
  font.setFamily(app.font().family())
  font.setPointSize(10)
  font.setWeight(QFont.Weight.Bold)

  app.setWindowIcon(images.GetAppIcon())
  app.setStyle("Fusion")
  app.setFont(font)
  app.setPalette(QtDarkTheme())

  mainwindow = MainWindow()
  sys.exit(app.exec())