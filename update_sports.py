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

circuit_flags = {
    "Bahrain International Circuit": "bh",
    "Jeddah Corniche Circuit": "sa",
    "Albert Park Grand Prix Circuit": "au",
    "Baku City Circuit": "az",
    "Miami International Autodrome": "us",
    "Circuit de Monaco": "mc",
    "Circuit Gilles Villeneuve": "ca",
    "Circuit de Barcelona-Catalunya": "es",
    "Red Bull Ring": "at",
    "Silverstone Circuit": "gb",
    "Hungaroring": "hu",
    "Circuit de Spa-Francorchamps": "be",
    "Circuit Zandvoort": "nl",
    "Monza Circuit": "it",
    "Marina Bay Street Circuit": "sg",
    "Circuit of the Americas": "us",
    "Autódromo Hermanos Rodríguez": "mx",
    "Autódromo José Carlos Pace": "br",
    "Las Vegas Strip Street Circuit": "us",
    "Losail International Circuit": "qa",
    "Losail": "qa",
    "Yas Marina Circuit": "ae",
    "Shanghai International Circuit": "cn",
    "Suzuka Circuit": "jp"
}

def fetch_f1_calendar():
    url = "https://api.jolpi.ca/ergast/f1/2026.json"
    events = []
    today_str = datetime.now().strftime('%Y-%m-%d')
    f1_logo = "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            races = data['MRData']['RaceTable']['Races']
            total_races = len(races)
            
            for i, race in enumerate(races):
                race_name = race['raceName']
                circuit_name = race['Circuit']['circuitName']
                flag_code = circuit_flags.get(circuit_name, "qa" if "Qatar" in race_name else "un")
                flag_url = f"https://flagcdn.com/w80/{flag_code}.png"
                gp_number = i + 1
                gp_label = f"GP {gp_number} / {total_races}"
                
                if 'Qualifying' in race:
                    q_date = race['Qualifying']['date']
                    q_time = adjust_hour(race['Qualifying'].get('time', '14:00:00')[:5], 1)
                    if q_date >= today_str:
                        events.append({
                            "id": f"f1_qual_{i}",
                            "date": q_date,
                            "category": "f1",
                            "sportIcon": f1_logo,
                            "isImgIcon": True,
                            "team1": race_name,
                            "team1Extra": "(Qualifications)",
                            "team1Logo": flag_url,
                            "team2": circuit_name,
                            "team2Logo": "",
                            "time": q_time,
                            "nature": gp_label,
                            "showHomeTeam1": False,
                            "channels": ["canal+"]
                        })

                if 'Sprint' in race:
                    s_date = race['Sprint']['date']
                    s_time = adjust_hour(race['Sprint'].get('time', '12:00:00')[:5], 1)
                    if s_date >= today_str:
                        events.append({
                            "id": f"f1_sprint_{i}",
                            "date": s_date,
                            "category": "f1",
                            "sportIcon": f1_logo,
                            "isImgIcon": True,
                            "team1": race_name,
                            "team1Extra": "(Course Sprint)",
                            "team1Logo": flag_url,
                            "team2": circuit_name,
                            "team2Logo": "",
                            "time": s_time,
                            "nature": gp_label,
                            "showHomeTeam1": False,
                            "channels": ["canal+"]
                        })

                r_date = race['date']
                r_time = adjust_hour(race.get('time', '14:00:00')[:5], 1)
                if r_date >= today_str:
                    events.append({
                        "id": f"f1_race_{i}",
                        "date": r_date,
                        "category": "f1",
                        "sportIcon": f1_logo,
                        "isImgIcon": True,
                        "team1": race_name,
                        "team1Extra": "(Course)",
                        "team1Logo": flag_url,
                        "team2": circuit_name,
                        "team2Logo": "",
                        "time": r_time,
                        "nature": gp_label,
                        "showHomeTeam1": False,
                        "channels": ["canal+"]
                    })
    except Exception as e:
        print(f"Erreur F1 : {e}")
    return events

def fetch_nfl_calendar():
    events = []
    seen_ids = set()
    today_str = datetime.now().strftime('%Y-%m-%d')
    nfl_logo = "https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png"
    
    phases = [
        (2, 19, 18),
        (3, 5, 4)
    ]
    
    for seasontype, max_weeks, total_weeks in phases:
        for week in range(1, max_weeks):
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype={seasontype}&week={week}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    if seasontype == 3:
                        nature_str = f"Play-offs ({week} / {total_weeks})"
                    else:
                        nature_str = f"Semaine {week} / {total_weeks}"

                    for i, event in enumerate(data.get('events', [])):
                        competition = event['competitions'][0]
                        date_iso = competition['date']
                        date_str = date_iso[:10]
                        
                        if date_str >= today_str:
                            event_id = event.get('id', f"nfl_st{seasontype}_w{week}_{i}")
                            if event_id not in seen_ids:
                                seen_ids.add(event_id)
                                raw_time = date_iso[11:16]
                                time_str = adjust_hour(raw_time, 1)
                                
                                venue = competition.get('venue')
                                if venue and venue.get('fullName'):
                                    venue_name = venue.get('fullName')
                                    venue_country = venue.get('address', {}).get('country', 'États-Unis')
                                    venue_info = f"{venue_name} ({venue_country})"
                                else:
                                    venue_info = "TBD"

                                competitors = competition['competitors']
                                team1 = competitors[0]
                                team2 = competitors[1]
                                
                                t1_name = team1['team'].get('displayName', 'TBD')
                                t2_name = team2['team'].get('displayName', 'TBD')
                                is_tbd = (t1_name == 'TBD' or t2_name == 'TBD')

                                events.append({
                                    "id": f"nfl_{event_id}",
                                    "date": date_str,
                                    "category": "nfl",
                                    "sportIcon": nfl_logo,
                                    "isImgIcon": True,
                                    "team1": t1_name,
                                    "team1Extra": "",
                                    "team1Logo": team1['team'].get('logo', ''),
                                    "showHomeTeam1": False if is_tbd else team1.get('homeAway') == 'home',
                                    "team2": t2_name,
                                    "team2Logo": team2['team'].get('logo', ''),
                                    "showHomeTeam2": False if is_tbd else team2.get('homeAway') == 'home',
                                    "venue": venue_info,
                                    "time": time_str,
                                    "nature": nature_str,
                                    "channels": ["beinsports", "dazn"]
                                })
            except Exception as e:
                pass
    return events

def fetch_nba_calendar():
    events = []
    seen_ids = set()
    today_str = datetime.now().strftime('%Y-%m-%d')
    nba_logo = "https://a.espncdn.com/i/teamlogos/leagues/500/nba.png"
    
    # NBA : Saison régulière (seasontype=2, semaines 1 à ~26) + Play-offs / Play-in (seasontype=3 ou 4)
    phases = [
        (2, 27, "Saison Régulière"),
        (3, 5, "Play-offs NBA")
    ]
    
    for seasontype, max_weeks, phase_label in phases:
        for week in range(1, max_weeks):
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?seasontype={seasontype}&week={week}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    for i, event in enumerate(data.get('events', [])):
                        competition = event['competitions'][0]
                        date_iso = competition['date']
                        date_str = date_iso[:10]
                        
                        if date_str >= today_str:
                            event_id = event.get('id', f"nba_st{seasontype}_w{week}_{i}")
                            if event_id not in seen_ids:
                                seen_ids.add(event_id)
                                raw_time = date_iso[11:16]
                                time_str = adjust_hour(raw_time, 1)
                                
                                venue = competition.get('venue')
                                if venue and venue.get('fullName'):
                                    venue_name = venue.get('fullName')
                                    venue_country = venue.get('address', {}).get('country', 'États-Unis')
                                    venue_info = f"{venue_name} ({venue_country})"
                                else:
                                    venue_info = "TBD"

                                competitors = competition['competitors']
                                team1 = competitors[0]
                                team2 = competitors[1]
                                
                                t1_name = team1['team'].get('displayName', 'TBD')
                                t2_name = team2['team'].get('displayName', 'TBD')
                                is_tbd = (t1_name == 'TBD' or t2_name == 'TBD')

                                events.append({
                                    "id": f"nba_{event_id}",
                                    "date": date_str,
                                    "category": "nba",
                                    "sportIcon": nba_logo,
                                    "isImgIcon": True,
                                    "team1": t1_name,
                                    "team1Extra": "",
                                    "team1Logo": team1['team'].get('logo', ''),
                                    "showHomeTeam1": False if is_tbd else team1.get('homeAway') == 'home',
                                    "team2": t2_name,
                                    "team2Logo": team2['team'].get('logo', ''),
                                    "showHomeTeam2": False if is_tbd else team2.get('homeAway') == 'home',
                                    "venue": venue_info,
                                    "time": time_str,
                                    "nature": phase_label,
                                    "channels": ["beinsports", "dazn"]
                                })
            except Exception as e:
                pass
    return events

def main():
    f1_events = fetch_f1_calendar()
    nfl_events = fetch_nfl_calendar()
    nba_events = fetch_nba_calendar()
    
    all_events = f1_events + nfl_events + nba_events
    all_events.sort(key=lambda x: (x['date'], x['time']))
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
