import importlib

tabsList = {
  "Suivi des séries": importlib.import_module("tabs.suivi_series").TabWidget(),
  "Convertisseur Base64": importlib.import_module("tabs.base64").TabWidget(),
  "Sélecteur de couleur": importlib.import_module("tabs.colorpicker").TabWidget(),
  "Maintenance du PC": importlib.import_module("tabs.maintenance").TabWidget(),
  "Résolutions par ratio d'aspect": importlib.import_module("tabs.resolutions").TabWidget(),
}
