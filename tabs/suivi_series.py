import bson
import images
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from requests.models import HTTPError
import tmdbsimple as tmdb
from variables import widgetMargins, TextShadow


tmdb_key_path = "tmdb.key"
tmdb_cache_path = "tmdb.dat"


class TabWidget(QWidget):
  serieStruct ={
    'name': "",
    'cover': bytes(0),
    'description': "",
    'seasons': [],
    'lastWatchedSeason': 1,
    'lastWatchedEpisode': 1
  }
  seriesContainer = []
  savedData = True


  def __init__(self):
    super().__init__()

    # LEFT SIDE
    self.seriesListBox = QListWidget()
    self.seriesListBox.currentItemChanged.connect(self.SeriesListBox_Changed)
    addSerieButton = QPushButton("Ajouter série")
    addSerieButton.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    addSerieButton.setStyleSheet("color: #0f0; font-weight: bold")
    addSerieButton.clicked.connect(self.AddSerie_Clicked)
    removeSerieButton = QPushButton("Supprimer série")
    removeSerieButton.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    removeSerieButton.setStyleSheet("color: #f33; font-weight: bold")
    removeSerieButton.clicked.connect(self.RemoveSerie_Clicked)

    leftLayout = QGridLayout()
    leftLayout.addWidget(self.seriesListBox, 0, 0, 1, 2)
    leftLayout.addWidget(addSerieButton, 1, 0)
    leftLayout.addWidget(removeSerieButton, 1, 1)

    leftGroupBox = QGroupBox("Liste des séries")
    leftGroupBox.setFixedWidth(250)
    leftGroupBox.setLayout(leftLayout)

    # RIGHT SIDE
    self.titleLabel = QLabel()
    self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.titleLabel.setContentsMargins(0, 10, 0, 10)
    self.titleLabel.setStyleSheet("color: #aaffff; font-size: 24px")
    self.titleLabel.setGraphicsEffect(TextShadow())
    self.coverBox = QLabel()
    self.coverBox.setGraphicsEffect(TextShadow())
    self.coverBox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.coverBox.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
    self.coverBox.setMinimumHeight(300)

    self.descriptionLabel = QLabel()
    self.descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignJustify)
    self.descriptionLabel.setWordWrap(True)
    self.descriptionLabel.setMargin(20)
    self.descriptionLabel.setGraphicsEffect(TextShadow())

    self.lastWatchedSeasonComboBox = QComboBox()
    self.lastWatchedSeasonComboBox.setMaximumWidth(50)
    self.lastWatchedEpisodeComboBox = QComboBox()
    self.lastWatchedEpisodeComboBox.setMaximumWidth(50)

    self.lastAvailableSeasonNumber = QLabel("N/A")
    self.lastAvailableSeasonNumber.setStyleSheet("color: #aaffff")
    self.lastAvailableEpisodeNumber = QLabel("N/A")
    self.lastAvailableEpisodeNumber.setStyleSheet("color: #aaffff")

    self.availableGroupBoxLayout = QFormLayout()
    self.availableGroupBoxLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
    self.availableGroupBoxLayout.addRow(QLabel("Saison:"), self.lastAvailableSeasonNumber)
    self.availableGroupBoxLayout.addRow(QLabel("Episode:"), self.lastAvailableEpisodeNumber)

    availableGroupBox = QGroupBox("Disponible")
    availableGroupBox.setLayout(self.availableGroupBoxLayout)

    watchedGroupBoxLayout = QFormLayout()
    watchedGroupBoxLayout.addRow(QLabel("Saison:"), self.lastWatchedSeasonComboBox)
    watchedGroupBoxLayout.addRow(QLabel("Episode:"), self.lastWatchedEpisodeComboBox)

    watchedGroupBox = QGroupBox("Regardé")
    watchedGroupBox.setLayout(watchedGroupBoxLayout)

    scrapeButton = QPushButton("Scraper depuis TMDB")
    scrapeButton.clicked.connect(self.ScrapeButton_Clicked)

    saveButton = QPushButton("Sauvegarder les données")
    saveButton.setDefault(True)
    saveButton.clicked.connect(self.SaveData)

    self.saveStatus = QLabel()
    self.saveStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.saveStatus.setGraphicsEffect(TextShadow())
    self.saveStatus.setContentsMargins(0, 5, 0, 0)

    rightLayout = QGridLayout()
    rightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    rightLayout.addWidget(self.titleLabel, 0, 0, 1, 2)
    rightLayout.addWidget(self.coverBox, 1, 0, 1, 2)
    rightLayout.addWidget(self.descriptionLabel, 2, 0, 1, 2)
    rightLayout.addWidget(availableGroupBox, 3, 0)
    rightLayout.addWidget(watchedGroupBox, 3, 1)
    rightLayout.addWidget(scrapeButton, 4, 0)
    rightLayout.addWidget(saveButton, 4, 1)
    rightLayout.addWidget(self.saveStatus, 5, 1)

    self.rightGroupBox = QGroupBox("Informations sur la série")
    self.rightGroupBox.setLayout(rightLayout)

    mainLayout = QGridLayout()
    mainLayout.setContentsMargins(widgetMargins)
    mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    mainLayout.addWidget(leftGroupBox, 0, 0)
    mainLayout.addWidget(self.rightGroupBox, 0, 1)

    self.setLayout(mainLayout)
    self.LoadData()
    self.ReloadData()
    
  def SeriesListBox_Changed(self, item):
    for serie in self.seriesContainer:
      if item and serie['name'] == item.text():
        self.selectedSerie = serie
        self.rightGroupBox.show()
        try:
          self.lastWatchedSeasonComboBox.disconnect()
          self.lastWatchedEpisodeComboBox.disconnect()
        except Exception: pass
        self.lastWatchedSeasonComboBox.clear()
        self.lastWatchedEpisodeComboBox.clear()
        
        # NAME
        self.titleLabel.setText(serie['name'])
        
        # DESCRIPTION
        if serie['description']: self.descriptionLabel.setText(serie['description'])
        else: self.descriptionLabel.setText("Aucune description. Scrappez pour récupérer les données.")

        # COVER
        coverPixmap = QPixmap()
        if serie['cover']:
          coverPixmap.loadFromData(serie['cover'])
        else:
          coverPixmap = images.GetNoCoverPixmap()        
        self.coverBox.setPixmap(coverPixmap.scaled(self.coverBox.width(), self.coverBox.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        # SEASONS ET EPISODES
        if len(serie['seasons']) > 0:
          self.lastAvailableSeasonNumber.setText("%s" % len(serie['seasons']))
          self.lastAvailableEpisodeNumber.setText("%s" % serie['seasons'][len(serie['seasons'])-1]['episode_count'])  
          self.lastWatchedSeasonComboBox.addItems("%s" % x for x in range(1, len(serie['seasons']) + 1))
          self.lastWatchedSeasonComboBox.setCurrentIndex(serie['lastWatchedSeason'] - 1)
          self.lastWatchedEpisodeComboBox.addItems("%s" % x for x in range(1, serie['seasons'][serie['lastWatchedSeason'] - 1]['episode_count'] + 1))
          self.lastWatchedEpisodeComboBox.setCurrentIndex(serie['lastWatchedEpisode'] - 1)
        else:
          self.lastAvailableSeasonNumber.setText("N/A")
          self.lastAvailableEpisodeNumber.setText("N/A")  
          self.lastWatchedSeasonComboBox.addItems("%s" % x for x in range(1, 21))
          self.lastWatchedSeasonComboBox.setCurrentIndex(serie['lastWatchedSeason'] - 1)
          self.lastWatchedEpisodeComboBox.addItems("%s" % x for x in range(1, 31))
          self.lastWatchedEpisodeComboBox.setCurrentIndex(serie['lastWatchedEpisode'] - 1)
        self.lastWatchedSeasonComboBox.currentIndexChanged.connect(self.SeasonComboBox_Changed)
        self.lastWatchedEpisodeComboBox.currentIndexChanged.connect(self.EpisodeComboBox_Changed)
    if not self.savedData:
      self.saveStatus.setStyleSheet("color: indianred")
      self.saveStatus.setText("Base de données NON sauvegardée.")
        
  def AddSerie_Clicked(self):
    def AjouterSerie(name):
      serie = dict(self.serieStruct)
      serie['name'] = name
      serie['seasons'] = []
      self.seriesContainer.append(serie)
      dialog.close()
      self.savedData = False
      self.ReloadData()

    dialog = QDialog(self)
    titleLabel = QLabel("Entrez le nom de la série à ajouter")
    serieLineEdit = QLineEdit()
    serieLineEdit.setContentsMargins(0, 5, 0, 10)
    okButton = QPushButton("Ajouter")
    okButton.setAutoDefault(True)
    okButton.clicked.connect(lambda: AjouterSerie(serieLineEdit.text()))
    cancelButton = QPushButton("Annuler")
    cancelButton.clicked.connect(lambda: dialog.close())

    layout = QGridLayout()
    layout.addWidget(titleLabel, 0, 0, 1, 2)
    layout.addWidget(serieLineEdit, 1, 0, 1, 2)
    layout.addWidget(okButton, 2, 0)
    layout.addWidget(cancelButton, 2, 1)
    
    dialog.setWindowTitle("Ajout d'une série")
    dialog.setLayout(layout)
    dialog.show()
  
  def RemoveSerie_Clicked(self):
    if hasattr(self, "selectedSerie") and QMessageBox.warning(self, "Attention", f"Voulez-vous vraiment supprimer l'élément <{self.selectedSerie['name']}> ?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
      self.seriesContainer.remove(self.selectedSerie)
      self.savedData = False
      self.ReloadData()

  def SeasonComboBox_Changed(self, index):
    if len(self.selectedSerie['seasons']) > 0:
      self.lastWatchedEpisodeComboBox.clear()
      episodeCount = self.selectedSerie['seasons'][index]['episode_count']
      self.lastWatchedEpisodeComboBox.addItems("%s" % (x + 1) for x in range(episodeCount))
    self.selectedSerie['lastWatchedSeason'] = index + 1

  def EpisodeComboBox_Changed(self, index):
    self.selectedSerie['lastWatchedEpisode'] = index + 1

  def ScrapeButton_Clicked(self):
    import requests, os, io

    # BASE CONFIG
    if os.path.exists(tmdb_key_path):
      with io.open(tmdb_key_path, mode="r") as fp:
        for line in fp:
          if line[0] != "#" and line != "":
            tmdb.API_KEY = line
    else:
      QMessageBox.critical(self, "Erreur", f"Le fichier <{tmdb_key_path}> est introuvable dans le dossier de l'exécutable.")
      return

    try:
      config = tmdb.Configuration()
      configResponse = config.info()
      baseUrl = configResponse['images']['base_url'] + "w500"
      # SEARCH BY NAME
      search = tmdb.Search()
      searchResponse = search.tv(query=self.selectedSerie["name"], language="fr")
      seriesNames = list(x['name'] for x in searchResponse['results'])
      dialogResponse = QInputDialog().getItem(self, "Resultat de la recherche TMDB", "Sélectionnez la série correspondante dans la liste:", seriesNames, editable=False)

      if dialogResponse[1]:
        # FILL DATABASE
        tv = tmdb.TV(searchResponse['results'][seriesNames.index(dialogResponse[0])]['id'])
        tvResponse = tv.info()
        self.selectedSerie['name'] = tvResponse['name']
        self.selectedSerie['description'] = searchResponse['results'][seriesNames.index(dialogResponse[0])]['overview']
        if tvResponse['poster_path']:
            coverData = requests.get(baseUrl + tvResponse['poster_path'])
            self.selectedSerie['cover'] = coverData.content
        self.selectedSerie['seasons'] = []
        for season in tvResponse['seasons']:
          if season['season_number'] > 0:
            self.selectedSerie['seasons'].append({'episode_count': season['episode_count']})
        self.savedData = False
        self.ReloadData()
    except HTTPError as e:
      QMessageBox.critical(self, "Erreur", f"La requête TMDB API à retourné l'erreur suivante:\n\n{e}")

  def LoadData(self):
    file = QFile(tmdb_cache_path)
    if(file.open(QFile.OpenModeFlag.ReadOnly)):
      tmpSeries = bson.loads(file.read(file.size()))
      for tmpSerie in tmpSeries.values(): self.seriesContainer.append(tmpSerie)
      file.close()
    else: self.seriesContainer = []

  def ReloadData(self):
    try: del self.selectedSerie
    except Exception: pass
    self.rightGroupBox.hide()
    self.seriesContainer = sorted(self.seriesContainer, key=lambda k: k['name'])
    self.seriesListBox.clear()
    for serie in self.seriesContainer: self.seriesListBox.addItem(serie['name'])
    try: self.seriesListBox.setCurrentIndex(0)
    except Exception: pass

  def SaveData(self):
    file = QFile(tmdb_cache_path)
    if(file.open(QFile.OpenModeFlag.WriteOnly)):
      file.write(bson.encode_array(self.seriesContainer, list()))
      file.close()
      self.saveStatus.setStyleSheet("color: forestgreen")
      self.saveStatus.setText("Base de données sauvegardée.")
      self.savedData = True
    else:
      self.saveStatus.setStyleSheet("color: indianred")
      self.saveStatus.setText("Une erreur est survenue.")
      self.SaveData = False