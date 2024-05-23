from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class QtDarkTheme(QPalette):
  def __init__(self):
    super().__init__()

    self.setColor(QPalette.ColorRole.Window, QColor(41,44,51))
    self.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    self.setColor(QPalette.ColorRole.Base, QColor(15,15,15))
    self.setColor(QPalette.ColorRole.AlternateBase, QColor(41,44,51))
    self.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    self.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    self.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    self.setColor(QPalette.ColorRole.Button, QColor(41,44,51))
    self.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    self.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    self.setColor(QPalette.ColorRole.Highlight, QColor(100,100,225))
    self.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
