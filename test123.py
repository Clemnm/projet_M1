from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Med Board")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #E0FFFF;")

        self.initUI()

    def initUI(self):
        # Barre latérale gauche
        sidebar_left = QtWidgets.QFrame(self)
        sidebar_left.setGeometry(0, 0, 200, 600)
        sidebar_left.setStyleSheet("background-color: #40E0D0;")

        logo = QtWidgets.QLabel("Med Board", sidebar_left)
        logo.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        logo.setStyleSheet("color: white;")
        logo.setGeometry(50, 10, 100, 40)

        icons = ['🏠 Home', '📅 Calendar', '📁 Files', '👤 Users', '⚙ Settings']
        for i, icon in enumerate(icons):
            btn = QtWidgets.QPushButton(icon, sidebar_left)
            btn.setFont(QtGui.QFont('Helvetica', 14))
            btn.setStyleSheet("color: white; background-color: #40E0D0; border: none;")
            btn.setGeometry(10, 60 + i*50, 180, 40)

        logout_btn = QtWidgets.QPushButton('Logout →', sidebar_left)
        logout_btn.setFont(QtGui.QFont('Helvetica', 14))
        logout_btn.setStyleSheet("color: white; background-color: #40E0D0; border: none;")
        logout_btn.setGeometry(10, 540, 180, 40)

        # Section principale
        main_section = QtWidgets.QFrame(self)
        main_section.setGeometry(200, 0, 600, 600)
        main_section.setStyleSheet("background-color: #E0FFFF;")

        header = QtWidgets.QFrame(main_section)
        header.setGeometry(0, 0, 600, 50)
        header.setStyleSheet("background-color: #E0FFFF;")

        greeting = QtWidgets.QLabel("Hello, Ashley!", header)
        greeting.setFont(QtGui.QFont('Helvetica', 20, QtGui.QFont.Bold))
        greeting.setGeometry(20, 10, 200, 30)

        date = QtWidgets.QLabel("12 April 2020, Monday", header)
        date.setFont(QtGui.QFont('Helvetica', 14))
        date.setGeometry(220, 10, 200, 30)

        search_bar = QtWidgets.QLineEdit(header)
        search_bar.setFont(QtGui.QFont('Helvetica', 14))
        search_bar.setGeometry(430, 10, 150, 30)

        search_icon = QtWidgets.QLabel("🔍", header)
        search_icon.setFont(QtGui.QFont('Helvetica', 14))
        search_icon.setGeometry(590, 10, 30, 30)

        # Carte de bienvenue
        welcome_card = QtWidgets.QFrame(main_section)
        welcome_card.setGeometry(20, 60, 560, 80)
        welcome_card.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

        welcome_msg = QtWidgets.QLabel("Welcome back...", welcome_card)
        welcome_msg.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        welcome_msg.setGeometry(20, 10, 200, 30)

        illustration = QtWidgets.QLabel("👩‍💻", welcome_card)
        illustration.setFont(QtGui.QFont('Helvetica', 40))
        illustration.setGeometry(230, 10, 40, 60)

        help_msg = QtWidgets.QLabel("I hope you're well, how can I help you?", welcome_card)
        help_msg.setFont(QtGui.QFont('Helvetica', 14))
        help_msg.setGeometry(280, 10, 250, 30)

        add_icon = QtWidgets.QLabel("➕", welcome_card)
        add_icon.setFont(QtGui.QFont('Helvetica', 20))
        add_icon.setGeometry(530, 10, 30, 30)

        # Carte des résultats médicaux
        results_card = QtWidgets.QFrame(main_section)
        results_card.setGeometry(20, 150, 560, 80)
        results_card.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

        results_title = QtWidgets.QLabel("Latest Results", results_card)
        results_title.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        results_title.setGeometry(20, 10, 200, 30)

        results_values = QtWidgets.QLabel("Glucose: 82 mg\nBUN: 10.5\nAST: 43.6", results_card)
        results_values.setFont(QtGui.QFont('Helvetica', 14))
        results_values.setGeometry(20, 40, 200, 30)

        # Cartes de navigation
        nav_cards = QtWidgets.QFrame(main_section)
        nav_cards.setGeometry(20, 240, 560, 100)
        nav_cards.setStyleSheet("background-color: #E0FFFF;")

        nav_labels = ['Diagnosis', 'Tests', 'Drugs']
        nav_icons = ['📁', '🔬', '💊']
        for i, (label, icon) in enumerate(zip(nav_labels, nav_icons)):
            card = QtWidgets.QFrame(nav_cards)
            card.setGeometry(10 + i*180, 10, 150, 80)
            card.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

            nav_icon = QtWidgets.QLabel(icon, card)
            nav_icon.setFont(QtGui.QFont('Helvetica', 40))
            nav_icon.setGeometry(50, 10, 50, 50)

            nav_label = QtWidgets.QLabel(label, card)
            nav_label.setFont(QtGui.QFont('Helvetica', 14))
            nav_label.setGeometry(40, 60, 100, 30)

        # Calendrier mensuel
        calendar_card = QtWidgets.QFrame(main_section)
        calendar_card.setGeometry(20, 350, 560, 100)
        calendar_card.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

        calendar_title = QtWidgets.QLabel("September", calendar_card)
        calendar_title.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        calendar_title.setGeometry(20, 10, 200, 30)

        calendar_days = QtWidgets.QLabel("  S  M  T  W  T  F  S\n 1  2  3  4  5  6  7\n 8  9 10 11 12 13 14\n15 16 17 18 19 20 21\n22 23 24 25 26 27 28\n29 30", calendar_card)
        calendar_days.setFont(QtGui.QFont('Helvetica', 14))
        calendar_days.setGeometry(20, 40, 200, 60)

        # Carte d'appointement
        appointment_card = QtWidgets.QFrame(main_section)
        appointment_card.setGeometry(20, 460, 560, 80)
        appointment_card.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

        appointment_details = QtWidgets.QLabel("Dr. Schmitz\n11:30 - 12:00", appointment_card)
        appointment_details.setFont(QtGui.QFont('Helvetica', 14))
        appointment_details.setGeometry(20, 10, 200, 60)

        calendar_icon = QtWidgets.QLabel("📅", appointment_card)
        calendar_icon.setFont(QtGui.QFont('Helvetica', 40))
        calendar_icon.setGeometry(230, 10, 40, 60)

        done_button = QtWidgets.QPushButton("Done", appointment_card)
        done_button.setFont(QtGui.QFont('Helvetica', 14))
        done_button.setStyleSheet("background-color: #ADD8E6;")
        done_button.setGeometry(280, 20, 80, 40)

        # Barre latérale droite
        sidebar_right = QtWidgets.QFrame(self)
        sidebar_right.setGeometry(800, 0, 200, 600)
        sidebar_right.setStyleSheet("background-color: #E0FFFF;")

        profile_pic = QtWidgets.QLabel("👤", sidebar_right)
        profile_pic.setFont(QtGui.QFont('Helvetica', 40))
        profile_pic.setGeometry(80, 10, 40, 40)

        user_info = QtWidgets.QLabel("Ashley Black\nashley.black@gmail.com", sidebar_right)
        user_info.setFont(QtGui.QFont('Helvetica', 14))
        user_info.setGeometry(20, 60, 160, 60)
        user_info.setAlignment(QtCore.Qt.AlignCenter)

        medical_info = QtWidgets.QLabel("Blood Group: A+\nHeight: 164 cm\nWeight: 57 kg", sidebar_right)
        medical_info.setFont(QtGui.QFont('Helvetica', 14))
        medical_info.setGeometry(20, 130, 160, 60)

        recent_results = QtWidgets.QFrame(sidebar_right)
        recent_results.setGeometry(20, 200, 160, 80)
        recent_results.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

        recent_results_title = QtWidgets.QLabel("Recent Results", recent_results)
        recent_results_title.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        recent_results_title.setGeometry(10, 10, 140, 30)

        recent_results_text = QtWidgets.QLabel("Latest medical result details...", recent_results)
        recent_results_text.setFont(QtGui.QFont('Helvetica', 14))
        recent_results_text.setGeometry(10, 40, 140, 30)

        reminders = QtWidgets.QFrame(sidebar_right)
        reminders.setGeometry(20, 290, 160, 80)
        reminders.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")

        reminders_title = QtWidgets.QLabel("Reminders", reminders)
        reminders_title.setFont(QtGui.QFont('Helvetica', 16, QtGui.QFont.Bold))
        reminders_title.setGeometry(10, 10, 140, 30)

        reminders_list = QtWidgets.QLabel("Email from Dr. Rogan\nEmail from Dr. Wolfhard\nEmail from Dermatologist", reminders)
        reminders_list.setFont(QtGui.QFont('Helvetica', 14))
        reminders_list.setGeometry(10, 40, 140, 30)

        tabs = QtWidgets.QFrame(sidebar_right)
        tabs.setGeometry(20, 380, 160, 40)
        tabs.setStyleSheet("background-color: #E0FFFF;")

        for i, tab in enumerate(['Documents', 'Contacts', 'Address']):
            tab_btn = QtWidgets.QPushButton(tab, tabs)
            tab_btn.setFont(QtGui.QFont('Helvetica', 14))
            tab_btn.setStyleSheet("background-color: #E0FFFF;")
            tab_btn.setGeometry(i*55, 0, 55, 40)

        add_remove_buttons = QtWidgets.QFrame(sidebar_right)
        add_remove_buttons.setGeometry(20, 430, 160, 40)
        add_remove_buttons.setStyleSheet("background-color: #E0FFFF;")

        add_btn = QtWidgets.QPushButton("+", add_remove_buttons)
        add_btn.setFont(QtGui.QFont('Helvetica', 14))
        add_btn.setStyleSheet("background-color: #ADD8E6;")
        add_btn.setGeometry(10, 0, 60, 40)

        remove_btn = QtWidgets.QPushButton("-", add_remove_buttons)
        remove_btn.setFont(QtGui.QFont('Helvetica', 14))
        remove_btn.setStyleSheet("background-color: #ADD8E6;")
        remove_btn.setGeometry(90, 0, 60, 40)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
