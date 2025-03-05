import tobii_research as tr

# Récupérer les périphériques connectés
found_eyetrackers = tr.find_all_eyetrackers()

if found_eyetrackers:
    print(f"Eyetracker trouvé : {found_eyetrackers[0].hostname}")
else:
    print("Aucun Eyetracker trouvé")

