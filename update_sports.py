import json
import urllib.request
from datetime import datetime

def fetch_f1_calendar():
    url = "https://api.jolpi.ca/ergast/f1/2026.json"
    events = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            races = data['MRData']['RaceTable']['Races']
            for i, race in enumerate(races):
                date_str = race['date']
                time_str = race.get('time', '15:00:00')[:5]
                if date_str >= datetime.now().strftime('%Y-%m-%d'):
                    events.append({
                        "id": f"f1_{i}",
                        "date": date_str,
                        "category": "f1",
                        "sportIcon": "fa-flag-checkered",
                        "team1": race['raceName'],
                        "team1Logo": "https://flagcdn.com/w80/un.png",
                        "team2": race['Circuit']['circuitName'],
                        "team2Logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Circuit_Mexico.svg/1024px-Circuit_Mexico.svg.png",
                        "time": time_str,
                        "channels": ["canal+"]
                    })
    except Exception as e:
        print(f"Erreur F1 : {e}")
    return events

def fetch_nfl_calendar():
    # Source de données publique et ouverte pour le planning de la NFL
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    events = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            for i, event in enumerate(data.get('events', [])):
                competition = event['competitions'][0]
                date_iso = competition['date'] # Format ISO (ex: 2026-10-28T00:15:00Z)
                date_str = date_iso[:10]
                time_str = date_iso[11:16] # Heure UTC qu'on peut ajuster si besoin
                
                competitors = competition['competitors']
                team1 = competitors[0]['team']['displayName']
                team1_logo = competitors[0]['team'].get('logo', '')
                team2 = competitors[1]['team']['displayName']
                team2_logo = competitors[1]['team'].get('logo', '')
                
                events.append({
                    "id": f"nfl_{i}",
                    "date": date_str,
                    "category": "nfl",
                    "sportIcon": "fa-football-ball",
                    "team1": team1,
                    "team1Logo": team1_logo,
                    "team2": team2,
                    "team2Logo": team2_logo,
                    "time": time_str,
                    "channels": ["beinsports", "dazn"]
                })
    except Exception as e:
        print(f"Erreur NFL : {e}")
    return events

def main():
    all_events = fetch_f1_calendar() + fetch_nfl_calendar()
    
    # Tri chronologique des événements
    all_events.sort(key=lambda x: (x['date'], x['time']))
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=4)
    
    print(f"Succès : {len(all_events)} événements totaux synchronisés (F1 + NFL).")

if __name__ == "__main__":
    main()
