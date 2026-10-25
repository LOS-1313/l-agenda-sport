import json
import urllib.request
from datetime import datetime, timedelta

def adjust_hour(time_str, hours_to_add=1):
    try:
        parts = time_str.split(':')
        dt = datetime.now().replace(hour=int(parts[0]), minute=int(parts[1])) + timedelta(hours=hours_to_add)
        return dt.strftime('%H:%M')
    except:
        return time_str

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
                raw_time = race.get('time', '14:00:00')[:5]
                time_str = adjust_hour(raw_time, 1)
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
    events = []
    seen_ids = set()
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # Parcourir les 18 semaines de la saison régulière NFL
    for week in range(1, 19):
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week={week}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                for i, event in enumerate(data.get('events', [])):
                    competition = event['competitions'][0]
                    date_iso = competition['date']
                    date_str = date_iso[:10]
                    
                    # On ne garde que les matchs futurs ou du jour
                    if date_str >= today_str:
                        event_id = event.get('id', f"nfl_w{week}_{i}")
                        if event_id not in seen_ids:
                            seen_ids.add(event_id)
                            raw_time = date_iso[11:16]
                            time_str = adjust_hour(raw_time, 1)
                            
                            competitors = competition['competitors']
                            team1 = competitors[0]['team']['displayName']
                            team1_logo = competitors[0]['team'].get('logo', '')
                            team2 = competitors[1]['team']['displayName']
                            team2_logo = competitors[1]['team'].get('logo', '')
                            
                            events.append({
                                "id": f"nfl_{event_id}",
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
            print(f"Erreur NFL semaine {week} : {e}")
            
    return events

def main():
    print("Récupération de la F1...")
    f1_events = fetch_f1_calendar()
    print(f"{len(f1_events)} événements F1 trouvés.")
    
    print("Récupération de l'intégralité de la saison NFL...")
    nfl_events = fetch_nfl_calendar()
    print(f"{len(nfl_events)} événements NFL trouvés.")
    
    all_events = f1_events + nfl_events
    all_events.sort(key=lambda x: (x['date'], x['time']))
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=4)
        
    print(f"Total : {len(all_events)} événements enregistrés dans data.json.")

if __name__ == "__main__":
    main()
