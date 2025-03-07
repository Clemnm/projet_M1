from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtCore import QTimer, QDateTime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import discord
from discord.ext import commands
import asyncio
import threading

# Spotify
# Configuration de l'authentification Spotify
SPOTIPY_CLIENT_ID = "27db069005f945268a968f9e51003941"
SPOTIPY_CLIENT_SECRET = "f28a390da20c45ff927d3fab3c9b9064"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))


# Messages
# Token du bot Discord
TOKEN = 'mettre le TOKEN'

# Initialiser les intents pour le bot Discord
intents = discord.Intents.default()
intents.message_content = True  # Permet au bot de lire et envoyer des messages

bot = commands.Bot(command_prefix="!", intents=intents)

# ID du contact à qui envoyer le message
contact_id = 794997006414250024  # L'ID du contact

# Liste des messages prédéfinis
messages = [
    "J'ai besoin d'aide.", "J'ai faim.", "J'ai soif.", "J'ai besoin d'aller aux toilettes.",
    "J’ai envie de discuter.", "Je ne me sens pas bien !", "Peux-tu me mettre au lit ?",
    "J'ai besoin d'envoyer un message, peux-tu m'aider ?"
]

#Domotique
# Configuration pour ConnectedSocket
BASE_URL = "http://10.10.195.32"
USERNAME = "ubnt"
PASSWORD = "ubnt"


class ConnectedSocket:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = None

    # Authentification de l'utilisateur et établissement de la session
    def authenticate(self):
        login_url = f"{BASE_URL}/login.cgi"
        data = {
            "username": USERNAME,
            "password": PASSWORD
        }
        response = self.session.post(login_url, data=data)
        response.raise_for_status()

        # Afficher tous les cookies pour débogage
        print(f"Cookies reçus : {self.session.cookies}")
        for cookie in self.session.cookies:
            if cookie.name == 'AIROS_SESSIONID':
                self.session_id = cookie.value
        if self.session_id:
            print("Authentification réussie")
        else:
            print("Échec de l'obtention de l'ID de session")

    # Obtenir une information spécifique d'une prise connectée
    def get_socket_info_key(self, socket_id, key):
        if not self.session_id:
            print("Vous devez vous authentifier d'abord")
            return None
        url = f"{BASE_URL}/sensors/{socket_id}/{key}"
        response = self.session.get(url)
        response.raise_for_status()

        # Vérifier si la réponse est une page de connexion
        if "Login" in response.text:
            print("Page de connexion reçue, réauthentification requise")
            self.authenticate()
            response = self.session.get(url)
            response.raise_for_status()

        # Vérifier si la réponse est vide ou non JSON
        if response.text.strip() == "":
            print("Réponse vide reçue")
            return None
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Échec de l'analyse de la réponse en JSON")
            print("Texte de la réponse :", response.text)
            return None

    # Basculer l'état d'une prise connectée
    def toggle_socket_state(self, socket_id):
        if not self.session_id:
            print("Vous devez vous authentifier d'abord")
            return
        current_state = self.get_socket_info_key(socket_id, "output")
        if current_state is None:
            print("Échec de la récupération de l'état actuel")
            return

        print(f"État actuel de la prise {socket_id} : {current_state}")

        # Extraire l'état actuel de la réponse JSON
        if isinstance(current_state, dict) and 'sensors' in current_state:
            sensors = current_state.get('sensors', [])
            if len(sensors) > 0 and 'output' in sensors[0]:
                current_state = sensors[0]['output']
            else:
                print("État actuel non trouvé dans la réponse")
                return
        else:
            print("État actuel non trouvé dans la réponse")
            return

        # Basculer l'état : passer à 1 si l'état actuel est 0, passer à 0 si l'état actuel est 1
        new_state = 1 if current_state == 0 else 0
        data = {"output": new_state}
        url = f"{BASE_URL}/sensors/{socket_id}"
        response = self.session.put(url, data=data)
        response.raise_for_status()
        print(f"État de la prise {socket_id} défini à {new_state}")


# Définition de la classe principale de la fenêtre principale de l'application.
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Définition du titre de la fenêtre et taille initiale de la fenêtre
        self.setWindowTitle("Med Board")
        self.resize(1000, 600)  # Permet le redimensionnement dynamique
        self.setStyleSheet("background-color:rgb(255, 255, 255);")

        # Initialisation de l'interface utilisateur
        self.initUI()
        self.light_on = False  # État initial de la lumière (éteinte)
        self.button_on = False  # État initial de l'appel d'urgence (désactivé)
        self.music_on = False  # État initial de la musique (désactivée)

        # Initialisation de ConnectedSocket
        self.connected_socket = ConnectedSocket()
        self.connected_socket.authenticate()  # Authentification lors de l'initialisation



    def initUI(self):
        # Création d'un widget central (zone de contenu principal de la fenêtre)
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        
        # Disposition horizontale pour organiser les blocs (barres latérales et section principale)
        main_layout = QtWidgets.QHBoxLayout(main_widget)

        # ----------------------------------------
        # Bloc de la barre latérale gauche
        sidebar_left = QtWidgets.QFrame()
        sidebar_left.setStyleSheet("background-color: #50B3C2; border-radius: 15px;")
        sidebar_left.setFixedWidth(200)  # Fixe la largeur de la barre latérale gauche

        # Disposition verticale des éléments dans la barre latérale gauche
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar_left)
        sidebar_layout.setSpacing(10)  # Définit l'espacement entre les éléments

        # Label de titre
        logo = QtWidgets.QLabel("Med Board")
        logo.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        logo.setStyleSheet("color: white;")
        logo.setAlignment(QtCore.Qt.AlignCenter)  # Centre le texte
        sidebar_layout.addWidget(logo)

        sidebar_layout.addStretch()
        # Bouton pour appeler l'urgence
        emergency_btn = QtWidgets.QPushButton('📞 Appel d\'urgence')
        emergency_btn.setFont(QtGui.QFont('Helvetica', 14))
        emergency_btn.setStyleSheet("color: white; background-color: #FF6347; border: none;")
        emergency_btn.setFixedSize(175, 400)
        sidebar_layout.addWidget(emergency_btn)

        # Ajout d'un espace flexible pour pousser le contenu vers le haut
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar_left)  # Ajoute la barre latérale gauche à la disposition principale

        # ----------------------------------------
        # Section principale
        main_section = QtWidgets.QFrame()
        main_section.setStyleSheet("background-color: #F4F8F9; border-radius: 15px;")  # Définition d'un fond clair
        main_layout.addWidget(main_section)

        # Disposition verticale pour organiser les éléments de la section principale
        main_section_layout = QtWidgets.QVBoxLayout(main_section)
        main_section_layout.setContentsMargins(20, 20, 20, 20)  # Définit les marges autour
        main_section_layout.setSpacing(20)  # Espacement entre les éléments

        # ----------------------------------------
        # En-tête (greeting + heure + date)
        header = QtWidgets.QFrame()
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)  # Enlève les marges autour
        header_layout.setSpacing(10)

        # Texte de bienvenue
        greeting = QtWidgets.QLabel("Bonjour et bienvenue !")
        greeting.setFont(QtGui.QFont('Helvetica', 20, QtGui.QFont.Bold))
        header_layout.addWidget(greeting)

        # Initialisation des labels pour afficher l'heure et la date
        self.time_label = QtWidgets.QLabel("", self)
        self.time_label.setFont(QtGui.QFont('Helvetica', 18))
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)

        self.date_label = QtWidgets.QLabel("", self)
        self.date_label.setFont(QtGui.QFont('Helvetica', 14))
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)

        # Ajout des labels de l'heure et de la date à l'en-tête
        header_layout.addWidget(self.time_label)
        header_layout.addWidget(self.date_label)

        # Mise à jour de l'heure en temps réel (chaque seconde)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)  # Connexion à la méthode update_time pour mise à jour
        self.timer.start(1000)  # Mise à jour toutes les secondes

        header_layout.addStretch()

        main_section_layout.addWidget(header)

        # ----------------------------------------
        # Disposition des boutons (Musique, Lumière, Message)
        button_layout = QtWidgets.QHBoxLayout()

        # Bouton Musique
        music_btn = QtWidgets.QPushButton("Musique")
        music_btn.setFont(QtGui.QFont('Helvetica', 18))  # Augmenter la taille de la police
        music_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px;  color: white;")
        music_btn.setFixedSize(200, 60)  # Taille fixe du bouton
        music_btn.clicked.connect(self.open_music_page)
        button_layout.addWidget(music_btn)

        # Bouton Lumière
        light_btn = QtWidgets.QPushButton("Lumière")
        light_btn.setFont(QtGui.QFont('Helvetica', 18))  # Augmenter la taille de la police
        light_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px;  color: white;")
        light_btn.setFixedSize(200, 60)  # Taille fixe du bouton
        light_btn.clicked.connect(self.toggle_light)  # Connexion du bouton à la fonction toggle_light
        button_layout.addWidget(light_btn)

        # Bouton Message
        message_btn = QtWidgets.QPushButton("Message")
        message_btn.setFont(QtGui.QFont('Helvetica', 18))  # Augmenter la taille de la police
        message_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px;  color: white;")
        message_btn.setFixedSize(200, 60)  # Taille fixe du bouton
        message_btn.clicked.connect(self.show_message_window)
        button_layout.addWidget(message_btn)

        main_section_layout.addLayout(button_layout) # Ajoute les boutons sous la forme d'une ligne horizontale

        # ----------------------------------------
        # Calendrier
        calendar = QtWidgets.QCalendarWidget()
        calendar.setGridVisible(True)  # Affiche la grille sur le calendrier
        calendar.setStyleSheet("background-color: #FFFFFF; border-radius: 15px;")
        main_section_layout.addWidget(calendar) 
        # ----------------------------------------
        # Barre latérale droite
        sidebar_right = QtWidgets.QFrame()
        sidebar_right.setStyleSheet("background-color: #cafafa; border-radius: 15px;")  # Couleur claire pour la barre droite
        sidebar_right.setFixedWidth(250)  # Fixe la largeur de la barre latérale droite

        # Disposition verticale des éléments dans la barre latérale droite
        sidebar_right_layout = QtWidgets.QVBoxLayout(sidebar_right)
        sidebar_right_layout.setSpacing(20)

        # Titre de la section Informations patients
        notifications_title = QtWidgets.QLabel("Informations patients")
        notifications_title.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        sidebar_right_layout.addWidget(notifications_title)
        
        # Photo de la personne (avec une image réelle réduite)
        photo_label = QtWidgets.QLabel()
        photo = QtGui.QPixmap("image.jpg")  # Remplace par le chemin de ton fichier image

        # Redimensionner l'image pour qu'elle soit plus petite tout en gardant ses proportions
        photo = photo.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # Appliquer l'image redimensionnée à l'étiquette
        photo_label.setPixmap(photo)
        photo_label.setAlignment(QtCore.Qt.AlignCenter)

        # Ajouter l'image au layout
        sidebar_right_layout.addWidget(photo_label)

        # Informations patient (nom, date de naissance, etc.)
        patient_info = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel("Nom: Sawssane Clémentine")
        patient_info.addWidget(name_label)

        dob_label = QtWidgets.QLabel("Date de naissance: 29/03/2203")
        patient_info.addWidget(dob_label)
        sidebar_right_layout.addLayout(patient_info)

        # Bloc Groupe sanguin, taille et poids
        info_block = QtWidgets.QVBoxLayout()
        blood_group_label = QtWidgets.QLabel("Groupe sanguin: B+")
        info_block.addWidget(blood_group_label)

        height_label = QtWidgets.QLabel("Taille: 175 cm")
        info_block.addWidget(height_label)

        weight_label = QtWidgets.QLabel("Poids: 85 kg")
        info_block.addWidget(weight_label)

        sidebar_right_layout.addLayout(info_block)

        sidebar_right_layout.addStretch()

        # Bloc Check-up
        checkup_block = QtWidgets.QVBoxLayout()
        checkup_title = QtWidgets.QLabel("Check-up")
        checkup_title.setFont(QtGui.QFont('Helvetica', 14, QtGui.QFont.Bold))
        checkup_block.addWidget(checkup_title)

        # Zone de texte (modifiable ou non)
        checkup_text = QtWidgets.QTextEdit()
        checkup_text.setPlainText("Médecin traitant : Dr Tomate\nDernier check-up réalisé : Sandra Gougena")
        checkup_text.setReadOnly(True)  # Si tu veux que ce soit seulement consultable et non modifiable
        checkup_block.addWidget(checkup_text)

        # Ajouter la disposition dans la barre latérale droite
        sidebar_right_layout.addLayout(checkup_block)


        # Bloc Préférences
        preferences_block = QtWidgets.QVBoxLayout()
        preferences_title = QtWidgets.QLabel("Préférences")
        preferences_title.setFont(QtGui.QFont('Helvetica', 14, QtGui.QFont.Bold))
        preferences_block.addWidget(preferences_title)

        preferences_text = QtWidgets.QTextEdit()
        preferences_text.setPlainText("Le patient aime sa température de bain à 35 °c")
        preferences_text.setReadOnly(True)  # Si tu veux que ce soit seulement consultable et non modifiable
        preferences_block.addWidget(preferences_text)

        # Ajouter la disposition dans la barre latérale droite
        sidebar_right_layout.addLayout(preferences_block)

        main_layout.addWidget(sidebar_right)  # Ajoute la barre latérale droite à la disposition principale

    def update_time(self):
        # Mise à jour de l'heure et de la date en temps réel
        current_time = QDateTime.currentDateTime()
        time_text = current_time.toString("HH:mm")  # Format de l'heure
        date_text = current_time.toString("dddd, dd MMMM yyyy")  # Format de la date

        # Mise à jour des labels affichant l'heure et la date
        self.time_label.setText(time_text)
        self.date_label.setText(date_text)

    def open_music_page(self):
        self.music_window = MusicWindow()
        self.music_window.show()
    
    # Fonction appelée lors de l'appel d'urgence
    def handle_emergency_call(self):
        print("Appel d'urgence activé !")  # Simuler un appel d'urgence

    def toggle_urgence(self):
        self.button_on = not self.button_on
        button_color = "#FF0000" if self.button_on else "#FF4D4D"  # Couleur de la lumière
        print(f"Appel {'activé' if self.button_on else 'désactivé'}")
        self.sender().setStyleSheet(f"background-color: {button_color}; border-radius: 15px; color: white;")  # Changer le style du bouton
    
        # Fonction pour allumer/éteindre la lumière
    def toggle_light(self):
        self.light_on = not self.light_on
        light_color = "#50b3c2" if self.light_on else "#B0E0E6"  # Couleur de la lumière
        print(f"Lumière {'allumée' if self.light_on else 'éteinte'}")
        self.sender().setStyleSheet(f"background-color: {light_color}; border-radius: 15px; color: white;")  # Changer le style du bouton

        # Toggle the state of the connected socket
        self.connected_socket.toggle_socket_state(6)

    def show_message_window(self):
        self.message_window = QtWidgets.QDialog(self)
        self.message_window.setWindowTitle("Choisir un message")
        self.message_window.setFixedSize(600, 400)  # Augmenter la taille de la fenêtre de sélection de message

        layout = QtWidgets.QVBoxLayout(self.message_window)
        layout.setSpacing(20)  # Espacement entre les boutons

        for message in messages:
            message_btn = QtWidgets.QPushButton(message)
            message_btn.setFont(QtGui.QFont('Helvetica', 14))  # Taille de la police réduite pour un meilleur affichage
            message_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px; color: white;")
            message_btn.setFixedSize(550, 50)  # Ajuster la taille des boutons pour qu'ils soient bien visibles
            message_btn.clicked.connect(lambda _, m=message: self.send_message(m))
            layout.addWidget(message_btn)  # Ajouter les boutons un par un en vertical

        self.message_window.exec_()

    def send_message(self, selected_message):
        print(f"Message choisi : {selected_message}")

        # Utiliser create_task pour envoyer le message dans la boucle d'événements du bot
        bot.loop.create_task(self.send_message_discord(selected_message))
        self.message_window.accept()

    async def send_message_discord(self, message):
        try:
            # Récupère l'utilisateur via son ID
            user = await bot.fetch_user(contact_id)
           
            # Envoie le message privé
            await user.send(message)
            print("Message envoyé avec succès!")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")


class MusicWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Playlists Spotify")
        self.resize(600, 600)

        layout = QtWidgets.QVBoxLayout()

        self.playlist_list = QtWidgets.QListWidget()
        self.load_playlists()
        self.playlist_list.itemClicked.connect(self.select_playlist)
        layout.addWidget(self.playlist_list)

        self.cover_label = QtWidgets.QLabel()
        self.cover_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.cover_label)

        # Disposition horizontale pour les boutons de contrôle
        controls_layout = QtWidgets.QHBoxLayout()

        self.prev_btn = QtWidgets.QPushButton("Previous")
        self.prev_btn.clicked.connect(self.prev_track)
        controls_layout.addWidget(self.prev_btn)

        self.play_btn = QtWidgets.QPushButton("Play")
        self.play_btn.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_btn)

        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_playlist)
        controls_layout.addWidget(self.pause_btn)

        self.next_btn = QtWidgets.QPushButton("Next")
        self.next_btn.clicked.connect(self.next_track)
        controls_layout.addWidget(self.next_btn)

        layout.addLayout(controls_layout)

        self.setLayout(layout)

        # Nouvel état pour savoir si on est en pause
        self.is_paused = False

    def load_playlists(self):
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            item = QtWidgets.QListWidgetItem()
            item.setText(playlist['name'])
            item.setData(QtCore.Qt.UserRole, playlist['uri'])
            item.setData(QtCore.Qt.UserRole + 1, playlist['images'][0]['url'] if playlist['images'] else None)

            # Ajouter l'image de la playlist ou un carré gris
            if playlist['images']:
                image = QtGui.QImage()
                image.loadFromData(requests.get(playlist['images'][0]['url']).content)
                icon = QtGui.QIcon(QtGui.QPixmap(image))
            else:
                icon = QtGui.QIcon(QtGui.QPixmap(100, 100).fill(QtGui.QColor('gray')))
            
            item.setIcon(icon)
            self.playlist_list.addItem(item)

    def select_playlist(self, item):
        self.selected_playlist_uri = item.data(QtCore.Qt.UserRole)
        cover_url = item.data(QtCore.Qt.UserRole + 1)
        if cover_url:
            image = QtGui.QImage()
            image.loadFromData(requests.get(cover_url).content)
            self.cover_label.setPixmap(QtGui.QPixmap(image))
        else:
            self.cover_label.setPixmap(QtGui.QPixmap(100, 100).fill(QtGui.QColor('gray')))

    def play_pause(self):
        if not hasattr(self, 'selected_playlist_uri'):
            QtWidgets.QMessageBox.critical(self, "Erreur", "Aucune playlist sélectionnée. Veuillez en sélectionner une.")
            return

        if self.is_paused:
            # Reprendre la lecture au bon endroit
            sp.start_playback()
            self.is_paused = False
        else:
            # Démarrer une nouvelle playlist
            sp.start_playback(context_uri=self.selected_playlist_uri)

    def pause_playlist(self):
        sp.pause_playback()
        self.is_paused = True  # On marque que la lecture est en pause

    def next_track(self):
        sp.next_track()

    def prev_track(self):
        sp.previous_track()


def run_discord_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())  # Crée une nouvelle boucle d'événements pour le thread
    bot.run(TOKEN)

# Démarrer le bot Discord dans un thread séparé
discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
discord_thread.start()


# Initialisation de l'application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())