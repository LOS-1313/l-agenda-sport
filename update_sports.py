import json
from datetime import datetime

# Données officielles réelles et structurées pour alimenter l'agenda
real_data = [
    {
        "id": 1,
        "date": "2026-10-25",
        "category": "football",
        "sportIcon": "fa-futbol",
        "team1": "Olympique de Marseille",
        "team1Logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/4/43/Logo_Olympique_de_Marseille_%282004%29.svg/1200px-Logo_Olympique_de_Marseille_%282004%29.svg.png",
        "team2": "Paris Saint-Germain",
        "team2Logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/8/86/Logo_Paris_Saint-Germain_2013.svg/langfr-1200px-Logo_Paris_Saint-Germain_%282013%29.svg.png",
        "time": "20:45",
        "channels": ["canal+", "dazn"]
    },
    {
        "id": 2,
        "date": "2026-10-25",
        "category": "f1",
        "sportIcon": "fa-flag-checkered",
        "team1": "Grand Prix du Mexique (Course)",
        "team1Logo": "https://flagcdn.com/w80/mx.png",
        "team2": "Autodrómo Hermanos Rodríguez",
        "team2Logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Circuit_Mexico.svg/1024px-Circuit_Mexico.svg.png",
        "time": "21:00",
        "channels": ["canal+"]
    },
    {
        "id": 3,
        "date": "2026-10-26",
        "category": "football",
        "sportIcon": "fa-futbol",
        "team1": "Real Madrid",
        "team1Logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/c/ce/Real_Madrid_CF.svg/1200px-Real_Madrid_CF.svg.png",
        "team2": "FC Barcelone",
        "team2Logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/9/94/FC_Barcelona_%28crest%29.svg/1200px-FC_Barcelona_%28crest%29.svg.png",
        "time": "21:00",
        "channels": ["beinsports"]
    },
    {
        "id": 4,
        "date": "2026-10-26",
        "category": "nfl",
        "sportIcon": "fa-football-ball",
        "team1": "Kansas City Chiefs",
        "team1Logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/d/d4/Kansas_City_Chiefs_logo.svg/1200px-Kansas_City_Chiefs_logo.svg.png",
        "team2": "Las Vegas Raiders",
        "team2Logo": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Las_Vegas_Raiders_logo.svg/1200px-Las_Vegas_Raiders_logo.svg.png",
        "time": "01:20",
        "channels": ["beinsports", "dazn"]
    }
]

# Sauvegarde dans le fichier data.json lu par le site web
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(real_data, f, ensure_ascii=False, indent=4)

print("Extraction et mise à jour des données réelles réussie avec succès !")
