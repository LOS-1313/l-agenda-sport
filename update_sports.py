import json
import urllib.request
from datetime import datetime

def fetch_f1_calendar():
    # URL de l'API ouverte officielle pour le calendrier F1 de la saison en cours (2026)
    url = "https://api.jolpi.ca/ergast/f1/2026.json"
    events = []
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            races = data['MRData']['RaceTable']['Races']
            
            for i, race in enumerate(races):
                race_name = race['raceName']
                date_str = race['date'] # Format YYYY-MM-DD
                time_str = race.get('time', '15:00:00')[:5] # Heure UTC par défaut
                
                # Filtrer pour ne garder que les courses à venir ou d'aujourd'hui
                if date_str >= datetime.now().strftime('%Y-%m-%d'):
                    events.append({
                        "id": i + 1,
                        "date": date_str,
                        "category": "f1",
                        "sportIcon": "fa-flag-checkered",
                        "team1": race_name,
                        "team1Logo": "https://flagcdn.com/w80/un.png",
                        "team2": race['Circuit']['circuitName'],
                        "team2Logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Circuit_Mexico.svg/1024px-Circuit_Mexico.svg.png",
                        "time": time_str,
                        "channels": ["canal+"]
                    })
    except Exception as e:
        print(f"Erreur lors de la récupération F1 : {e}")
        
    return events

def main():
    f1_events = fetch_f1_calendar()
    
    # Sauvegarde dans data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(f1_events, f, ensure_ascii=False, indent=4)
    
    print(f"Succès : {len(f1_events)} Grands Prix F1 officiels récupérés.")

if __name__ == "__main__":
    main()
