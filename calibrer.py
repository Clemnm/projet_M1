import tobii_research as tr
import pyautogui
import time
import tkinter as tk

# Trouver l'eyetracker
eyetracker = tr.find_all_eyetrackers()[0]

# Calibration : 4 points à viser sur l'écran du projecteur
calibration_points = [
    (0.1, 0.1),  # Point en haut à gauche
    (0.9, 0.1),  # Point en haut à droite
    (0.9, 0.9),  # Point en bas à droite
    (0.1, 0.9)   # Point en bas à gauche
]

# Création de la fenêtre principale de l'interface
root = tk.Tk()
root.title("Calibration Tobii Pro Glasses 3")

# Taille de la fenêtre (écran complet)
screen_width, screen_height = pyautogui.size()
root.geometry(f"{screen_width}x{screen_height}+0+0")  # Utilisation de toute la taille de l'écran

# Fonction de calibration : Afficher les 4 points et attendre le regard de l'utilisateur
def calibrate():
    print("Calibration des lunettes - Regardez les points sur l'écran")
    for point in calibration_points:
        # Afficher le carré à l'écran (dans le projet vidéo)
        x, y = point
        # Convertir les coordonnées relatives (0,1) en pixels
        screen_width, screen_height = pyautogui.size()
        x_pixel = int(x * screen_width)
        y_pixel = int(y * screen_height)

        # Créer un rectangle sur la fenêtre Tkinter pour chaque point
        square_size = 50  # Taille du carré
        square = tk.Canvas(root, width=square_size, height=square_size, bg="red")
        square.place(x=x_pixel - square_size // 2, y=y_pixel - square_size // 2)

        # Attendre que l'utilisateur regarde ce point pendant 2 secondes
        time.sleep(2)

        # Retirer le carré après 2 secondes
        square.destroy()

# Callback de suivi du regard pour déplacer le curseur
def calibration_callback(gaze_data):
    # Récupérer les coordonnées du regard
    gaze_x = gaze_data.gaze_point_on_display_area[0]
    gaze_y = gaze_data.gaze_point_on_display_area[1]

    # Mapper les coordonnées sur la taille de l'écran
    screen_width, screen_height = pyautogui.size()
    x = gaze_x * screen_width
    y = gaze_y * screen_height

    # Déplacer la souris
    pyautogui.moveTo(x, y)

# Lancer la calibration
def start_calibration():
    calibrate()

# Lancer la collecte des données de regard pour utiliser les lunettes comme souris
def start_gaze_tracking():
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, calibration_callback, as_dictionary=True)

# Fonction pour arrêter le suivi des données
def stop_gaze_tracking():
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, calibration_callback)

# Interface graphique pour démarrer la calibration
start_button = tk.Button(root, text="Démarrer Calibration", command=start_calibration, font=("Arial", 20))
start_button.pack(pady=20)

# Interface graphique pour démarrer le suivi du regard
track_button = tk.Button(root, text="Commencer Suivi Regard", command=start_gaze_tracking, font=("Arial", 20))
track_button.pack(pady=20)

# Interface graphique pour arrêter le suivi du regard
stop_button = tk.Button(root, text="Arrêter Suivi Regard", command=stop_gaze_tracking, font=("Arial", 20))
stop_button.pack(pady=20)

# Lancer la boucle principale de l'interface graphique
root.mainloop()
