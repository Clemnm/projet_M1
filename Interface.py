# Importation des modules nécessaires pour PyQt5, ainsi que les outils de base pour l'interface graphique.
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtCore import QTimer, QDateTime

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
        button_layout.addWidget(music_btn)

        # Bouton Lumière
        light_btn = QtWidgets.QPushButton("Lumière")
        light_btn.setFont(QtGui.QFont('Helvetica', 18))  # Augmenter la taille de la police
        light_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px;  color: white;")
        light_btn.setFixedSize(200, 60)  # Taille fixe du bouton
        button_layout.addWidget(light_btn)

        # Bouton Message
        message_btn = QtWidgets.QPushButton("Message")
        message_btn.setFont(QtGui.QFont('Helvetica', 18))  # Augmenter la taille de la police
        message_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px;  color: white;")
        message_btn.setFixedSize(200, 60)  # Taille fixe du bouton
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
        photo = QtGui.QPixmap("/Users/clementine/Desktop/image_test.jpeg")  # Remplace par le chemin de ton fichier image

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

# Initialisation de l'application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()  # Création de la fenêtre principale
    window.show()  # Affichage de la fenêtre
    sys.exit(app.exec_())  # Exécution de l'application
#pipi de clodo