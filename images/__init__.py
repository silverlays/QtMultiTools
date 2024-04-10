import pkgutil
from PyQt6.QtGui import QIcon, QPixmap

def GetAppIcon() -> QIcon:
  icon = QIcon()
  pixmap = QPixmap()
  pixmap.loadFromData(pkgutil.get_data("images", "app.ico"))
  icon.addPixmap(pixmap)
  return icon

def GetNoCoverPixmap() -> QPixmap:
  pixmap = QPixmap()
  pixmap.loadFromData(pkgutil.get_data("images", "no-cover.jpg"))
  return pixmap

