from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtCore import QTimer, QDateTime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Med Board")
        self.resize(1000, 600)
        self.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.initUI()
        self.light_on = False
        self.music_on = False

    def initUI(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QHBoxLayout(main_widget)

        # Sidebar Left
        sidebar_left = QtWidgets.QFrame()
        sidebar_left.setStyleSheet("background-color: #50B3C2; border-radius: 15px;")
        sidebar_left.setFixedWidth(200)
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar_left)
        logo = QtWidgets.QLabel("Med Board")
        logo.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        logo.setStyleSheet("color: white;")
        logo.setAlignment(QtCore.Qt.AlignCenter)
        sidebar_layout.addWidget(logo)
        
        sidebar_layout.addStretch()
        emergency_btn = QtWidgets.QPushButton('📞 Appel d\'urgence')
        emergency_btn.setFont(QtGui.QFont('Helvetica', 14))
        emergency_btn.setStyleSheet("color: white; background-color: #FF6347; border: none;")
        emergency_btn.setFixedSize(175, 400)
        emergency_btn.clicked.connect(self.handle_emergency_call)
        sidebar_layout.addWidget(emergency_btn)
        
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar_left)

        # Main Section
        main_section = QtWidgets.QFrame()
        main_section.setStyleSheet("background-color: #F4F8F9; border-radius: 15px;")
        main_layout.addWidget(main_section)

        main_section_layout = QtWidgets.QVBoxLayout(main_section)
        main_section_layout.setContentsMargins(20, 20, 20, 20)
        main_section_layout.setSpacing(20)

        # Header
        header = QtWidgets.QFrame()
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        greeting = QtWidgets.QLabel("Bonjour et bienvenue !")
        greeting.setFont(QtGui.QFont('Helvetica', 20, QtGui.QFont.Bold))
        header_layout.addWidget(greeting)
        
        self.time_label = QtWidgets.QLabel("", self)
        self.time_label.setFont(QtGui.QFont('Helvetica', 18))
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)

        self.date_label = QtWidgets.QLabel("", self)
        self.date_label.setFont(QtGui.QFont('Helvetica', 14))
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)

        header_layout.addWidget(self.time_label)
        header_layout.addWidget(self.date_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        header_layout.addStretch()
        main_section_layout.addWidget(header)

        # Buttons (Music, Light, Message)
        button_layout = QtWidgets.QHBoxLayout()
        
        music_btn = QtWidgets.QPushButton("Musique")
        music_btn.setFont(QtGui.QFont('Helvetica', 18))
        music_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px; color: white;")
        music_btn.setFixedSize(200, 60)
        music_btn.clicked.connect(self.toggle_music)
        button_layout.addWidget(music_btn)

        light_btn = QtWidgets.QPushButton("Lumière")
        light_btn.setFont(QtGui.QFont('Helvetica', 18))
        light_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px; color: white;")
        light_btn.setFixedSize(200, 60)
        light_btn.clicked.connect(self.toggle_light)
        button_layout.addWidget(light_btn)

        message_btn = QtWidgets.QPushButton("Message")
        message_btn.setFont(QtGui.QFont('Helvetica', 18))
        message_btn.setStyleSheet("background-color: #50b3c2; border-radius: 15px; color: white;")
        message_btn.setFixedSize(200, 60)
        message_btn.clicked.connect(self.open_message_window)
        button_layout.addWidget(message_btn)

        main_section_layout.addLayout(button_layout)

        # Calendar
        calendar = QtWidgets.QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setStyleSheet("background-color: #FFFFFF; border-radius: 15px;")
        main_section_layout.addWidget(calendar)

        # Sidebar Right (Patient Info, Check-up, Preferences)
        sidebar_right = QtWidgets.QFrame()
        sidebar_right.setStyleSheet("background-color: #cafafa; border-radius: 15px;")
        sidebar_right.setFixedWidth(250)
        sidebar_right_layout = QtWidgets.QVBoxLayout(sidebar_right)
        sidebar_right_layout.setSpacing(20)

        notifications_title = QtWidgets.QLabel("Informations patients")
        notifications_title.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        sidebar_right_layout.addWidget(notifications_title)

        # Photo de la personne (avec une image réelle réduite)
        photo_label = QtWidgets.QLabel()
        photo = QtGui.QPixmap("projet_M1/image.jpg")  # Remplace par le chemin de ton fichier image

        # Redimensionner l'image pour qu'elle soit plus petite tout en gardant ses proportions
        photo = photo.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # Appliquer l'image redimensionnée à l'étiquette
        photo_label.setPixmap(photo)
        photo_label.setAlignment(QtCore.Qt.AlignCenter)

        # Ajouter l'image au layout
        sidebar_right_layout.addWidget(photo_label)

        # Patient Info
        patient_info = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel("Nom: Sawssane Clémentine")
        patient_info.addWidget(name_label)

        dob_label = QtWidgets.QLabel("Date de naissance: 29/03/2203")
        patient_info.addWidget(dob_label)
        
        # New patient info (Blood type, height, weight)
        blood_type_label = QtWidgets.QLabel("Groupe sanguin: O+")
        patient_info.addWidget(blood_type_label)
        
        height_label = QtWidgets.QLabel("Taille: 1.70 m")
        patient_info.addWidget(height_label)
        
        weight_label = QtWidgets.QLabel("Poids: 65 kg")
        patient_info.addWidget(weight_label)

        # Patient image (resize image)
        patient_image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("path/to/your/image.jpg")  # Change to actual image path
        patient_image.setPixmap(pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio))
        sidebar_right_layout.addWidget(patient_image)

        sidebar_right_layout.addLayout(patient_info)

        # Check-up Block
        checkup_block = QtWidgets.QVBoxLayout()
        checkup_title = QtWidgets.QLabel("Check-up")
        checkup_title.setFont(QtGui.QFont('Helvetica', 14, QtGui.QFont.Bold))
        checkup_block.addWidget(checkup_title)

        checkup_text = QtWidgets.QTextEdit()
        checkup_text.setPlainText("Médecin traitant : Dr Tomate\nDernier check-up réalisé : Sandra Gougena")
        checkup_text.setReadOnly(True)
        checkup_block.addWidget(checkup_text)

        sidebar_right_layout.addLayout(checkup_block)

        # Preferences Block
        preferences_block = QtWidgets.QVBoxLayout()
        preferences_title = QtWidgets.QLabel("Préférences")
        preferences_title.setFont(QtGui.QFont('Helvetica', 14, QtGui.QFont.Bold))
        preferences_block.addWidget(preferences_title)

        preferences_text = QtWidgets.QTextEdit()
        preferences_text.setPlainText("Préférences alimentaires : Végétarien\nAutres préférences : Temps de sommeil 8h")
        preferences_text.setReadOnly(True)
        preferences_block.addWidget(preferences_text)

        sidebar_right_layout.addLayout(preferences_block)

        main_layout.addWidget(sidebar_right)

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        time_text = current_time.toString("HH:mm")
        date_text = current_time.toString("dddd, dd MMMM yyyy")
        self.time_label.setText(time_text)
        self.date_label.setText(date_text)

    def handle_emergency_call(self):
        print("Appel d'urgence activé !")  # Simuler un appel d'urgence

    def toggle_music(self):
        self.music_on = not self.music_on
        print(f"Musique {'activée' if self.music_on else 'désactivée'}")

    def toggle_light(self):
        self.light_on = not self.light_on
        light_color = "#FFFF00" if self.light_on else "#B0E0E6"
        print(f"Lumière {'allumée' if self.light_on else 'éteinte'}")
        self.sender().setStyleSheet(f"background-color: {light_color}; border-radius: 15px; color: white;")

    def open_message_window(self):
        message_window = MessageWindow()
        message_window.exec_()

class MessageWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choisir un destinataire")
        self.setFixedSize(300, 200)
        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        contact_btns = [
            "Médecin", "Infirmière", "Urgences", "Famille"
        ]
        for contact in contact_btns:
            btn = QtWidgets.QPushButton(contact)
            btn.clicked.connect(lambda checked, contact=contact: self.select_contact(contact))
            layout.addWidget(btn)

    def select_contact(self, contact_name):
        print(f"Contact sélectionné: {contact_name}")
        message_window = MessageSelectionWindow(contact_name)
        message_window.exec_()

class MessageSelectionWindow(QtWidgets.QDialog):
    def __init__(self, contact_name):
        super().__init__()
        self.setWindowTitle(f"Messages pour {contact_name}")
        self.setFixedSize(300, 200)
        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        messages = [
            "J'ai besoin d'aide.", "J'ai faim.", "J'ai soif ?", "J'ai besoin d'aller aux toilettes.",
            "J’ai envie de discuter !", "Je ne me sens pas bien !", "Peux-tu me mettre au lit ?",
            "J'ai besoin d'envoyer un message, peux-tu m'aider ?"
        ]
        for message in messages:
            btn = QtWidgets.QPushButton(message)
            btn.clicked.connect(lambda checked, message=message: self.send_message(message))
            layout.addWidget(btn)

    def send_message(self, message):
        print(f"Message envoyé: {message}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
