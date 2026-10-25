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

def get_adjusted_datetime(date_str, time_str, hours_to_add=1):
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M") + timedelta(hours=hours_to_add)
        return dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M')
    except:
        return date_str, time_str

circuit_data = {
    "Bahrain International Circuit": {"flag": "bh", "city": "Sakhir"},
    "Jeddah Corniche Circuit": {"flag": "sa", "city": "Djeddah"},
    "Albert Park Grand Prix Circuit": {"flag": "au", "city": "Melbourne"},
    "Baku City Circuit": {"flag": "az", "city": "Bakou"},
    "Miami International Autodrome": {"flag": "us", "city": "Miami"},
    "Circuit de Monaco": {"flag": "mc", "city": "Monaco"},
    "Circuit Gilles Villeneuve": {"flag": "ca", "city": "Montréal"},
    "Circuit de Barcelona-Catalunya": {"flag": "es", "city": "Barcelone"},
    "Red Bull Ring": {"flag": "at", "city": "Spielberg"},
    "Silverstone Circuit": {"flag": "gb", "city": "Silverstone"},
    "Hungaroring": {"flag": "hu", "city": "Budapest"},
    "Circuit de Spa-Francorchamps": {"flag": "be", "city": "Spa-Francorchamps"},
    "Circuit Park Zandvoort": {"flag": "nl", "city": "Zandvoort"},
    "Autodromo Nazionale di Monza": {"flag": "it", "city": "Monza"},
    "Madring": {"flag": "es", "city": "Madrid"},
    "Sepang International Circuit": {"flag": "my", "city": "Sepang"},
    "Marina Bay Street Circuit": {"flag": "sg", "city": "Singapour"},
    "Circuit of the Americas": {"flag": "us", "city": "Austin"},
    "Autódromo Hermanos Rodríguez": {"flag": "mx", "city": "Mexico"},
    "Autódromo José Carlos Pace": {"flag": "br", "city": "São Paulo"},
    "Las Vegas Strip Street Circuit": {"flag": "us", "city": "Las Vegas"},
    "Losail International Circuit": {"flag": "qa", "city": "Lusail"},
    "Losail Circuit": {"flag": "qa", "city": "Lusail"},
    "Losail": {"flag": "qa", "city": "Lusail"},
    "Yas Marina Circuit": {"flag": "ae", "city": "Abou Dabi"},
    "Shanghai International Circuit": {"flag": "cn", "city": "Shanghai"},
    "Suzuka Circuit": {"flag": "jp", "city": "Suzuka"}
}

def check_f1_status(date_str, time_str, duration_hours=2):
    try:
        now = datetime.now()
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(hours=duration_hours)
        is_live = start_dt <= now <= end_dt
        is_finished = now > end_dt
        return is_live, is_finished
    except:
        return False, False

def fetch_f1_results(round_num, session_type="results"):
    url = f"https://api.jolpi.ca/ergast/f1/2026/{round_num}/{session_type}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            table_key = "RaceTable" if session_type == "results" else "QualifyingTable"
            races = data['MRData'][table_key]['Races']
            if not races:
                return ""
            
            key = "Results" if session_type == "results" else "QualifyingResults"
            results = races[0].get(key, [])
            
            lines = []
            for res in results[:10]:
                pos = res.get('position', '')
                driver = res['Driver']
                code = driver.get('code', driver['familyName'][:3].upper())
                lines.append(f"{pos}. {code}")
            return "<br>".join(lines)
    except:
        return ""

def fetch_f1_calendar():
    url = "https://api.jolpi.ca/ergast/f1/2026.json"
    events = []
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
                round_num = race['round']
                
                if "Qatar" in race_name or "Losail" in circuit_name:
                    info = {"flag": "qa", "city": "Lusail"}
                else:
                    info = circuit_data.get(circuit_name, {"flag": "un", "city": ""})

                flag_url = f"https://flagcdn.com/w80/{info['flag']}.png"
                circuit_display = f"{circuit_name} ({info['city']})" if info['city'] else circuit_name
                
                gp_number = i + 1
                gp_label = f"GP {gp_number} / {total_races}"
                
                if 'Qualifying' in race:
                    q_date_raw = race['Qualifying']['date']
                    q_time_raw = race['Qualifying'].get('time', '14:00:00')[:5]
                    q_date, q_time = get_adjusted_datetime(q_date_raw, q_time_raw, 1)
                    
                    is_live, is_finished = check_f1_status(q_date, q_time, 1)
                    score_str = fetch_f1_results(round_num, "qualifying") if is_finished or is_live else ""
                    events.append({
                        "id": f"f1_qual_{i}",
                        "date": q_date,
                        "category": "f1",
                        "sportIcon": f1_logo,
                        "isImgIcon": True,
                        "team1": race_name,
                        "team1Extra": "(Qualifications)",
                        "team1Logo": flag_url,
                        "team2": circuit_display,
                        "team2Logo": "",
                        "time": q_time,
                        "nature": gp_label,
                        "isLive": is_live,
                        "isFinished": is_finished,
                        "score": score_str,
                        "showHomeTeam1": False,
                        "channels": ["canal+"]
                    })

                if 'Sprint' in race:
                    s_date_raw = race['Sprint']['date']
                    s_time_raw = race['Sprint'].get('time', '12:00:00')[:5]
                    s_date, s_time = get_adjusted_datetime(s_date_raw, s_time_raw, 1)
                    
                    is_live, is_finished = check_f1_status(s_date, s_time, 1)
                    score_str = fetch_f1_results(round_num, "results") if is_finished or is_live else ""
                    events.append({
                        "id": f"f1_sprint_{i}",
                        "date": s_date,
                        "category": "f1",
                        "sportIcon": f1_logo,
                        "isImgIcon": True,
                        "team1": race_name,
                        "team1Extra": "(Course Sprint)",
                        "team1Logo": flag_url,
                        "team2": circuit_display,
                        "team2Logo": "",
                        "time": s_time,
                        "nature": gp_label,
                        "isLive": is_live,
                        "isFinished": is_finished,
                        "score": score_str,
                        "showHomeTeam1": False,
                        "channels": ["canal+"]
                    })

                r_date_raw = race['date']
                r_time_raw = race.get('time', '14:00:00')[:5]
                r_date, r_time = get_adjusted_datetime(r_date_raw, r_time_raw, 1)
                
                is_live, is_finished = check_f1_status(r_date, r_time, 2)
                score_str = fetch_f1_results(round_num, "results") if is_finished or is_live else ""
                events.append({
                    "id": f"f1_race_{i}",
                    "date": r_date,
                    "category": "f1",
                    "sportIcon": f1_logo,
                    "isImgIcon": True,
                    "team1": race_name,
                    "team1Extra": "(Course)",
                    "team1Logo": flag_url,
                    "team2": circuit_display,
                    "team2Logo": "",
                    "time": r_time,
                    "nature": gp_label,
                    "isLive": is_live,
                    "isFinished": is_finished,
                    "score": score_str,
                    "showHomeTeam1": False,
                    "channels": ["canal+"]
                })
    except Exception as e:
        print(f"Erreur F1 : {e}")
    return events

def fetch_espn_games(sport_path, category, phases):
    events = []
    seen_ids = set()
    logo_url = f"https://a.espncdn.com/i/teamlogos/leagues/500/{category}.png"
    
    for seasontype, max_weeks, total_weeks in phases:
        for week in range(1, max_weeks):
            url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_path}/scoreboard?seasontype={seasontype}&week={week}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    if category == "nfl":
                        nature_str = f"Play-offs ({week} / {total_weeks})" if seasontype == 3 else f"Semaine {week} / {total_weeks}"
                    else:
                        nature_str = "Play-offs NBA" if seasontype == 3 else "Saison Régulière"

                    for i, event in enumerate(data.get('events', [])):
                        competition = event['competitions'][0]
                        date_iso = competition['date']
                        date_str_raw = date_iso[:10]
                        raw_time = date_iso[11:16]
                        
                        # Ajustement heure +1h et report au lendemain si entre 00:00 et 00:59
                        date_str, time_str = get_adjusted_datetime(date_str_raw, raw_time, 1)

                        event_id = event.get('id', f"{category}_st{seasontype}_w{week}_{i}")
                        if event_id not in seen_ids:
                            seen_ids.add(event_id)
                            
                            status_type = event.get('status', {}).get('type', {})
                            status_state = status_type.get('state', 'pre')
                            is_live = (status_state == 'in')
                            is_finished = (status_state == 'post')

                            competitors = competition['competitors']
                            team1 = competitors[0]
                            team2 = competitors[1]
                            
                            t1_name = team1['team'].get('displayName', 'TBD')
                            t2_name = team2['team'].get('displayName', 'TBD')
                            is_tbd = (t1_name == 'TBD' or t2_name == 'TBD')

                            score_str = ""
                            if is_live or is_finished:
                                s1 = team1.get('score', '0')
                                s2 = team2.get('score', '0')
                                score_str = f"{s1} - {s2}"

                            venue = competition.get('venue')
                            if venue and venue.get('fullName'):
                                v_name = venue.get('fullName')
                                addr = venue.get('address', {})
                                v_city = addr.get('city', '')
                                v_country = addr.get('country', 'États-Unis')
                                venue_info = f"{v_name} ({v_city} - {v_country})" if v_city else f"{v_name} ({v_country})"
                            else:
                                venue_info = "TBD"

                            events.append({
                                "id": f"{category}_{event_id}",
                                "date": date_str,
                                "category": category,
                                "sportIcon": logo_url,
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
                                "isLive": is_live,
                                "isFinished": is_finished,
                                "score": score_str,
                                "channels": ["beinsports", "dazn"]
                            })
            except Exception as e:
                pass
    return events

def fetch_nba_calendar():
    events = []
    seen_ids = set()
    today_dt = datetime.now()
    nba_logo = "https://a.espncdn.com/i/teamlogos/leagues/500/nba.png"
    
    year = today_dt.year
    months = []
    for i in range(9):
        current_m = (today_dt.month - 1 + i) % 12 + 1
        current_y = year + (today_dt.month - 1 + i) // 12
        months.append(f"{current_y}{current_m:02d}")
    
    for month_str in months:
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={month_str}&limit=1000"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                for i, event in enumerate(data.get('events', [])):
                    competition = event['competitions'][0]
                    date_iso = competition['date']
                    date_str_raw = date_iso[:10]
                    raw_time = date_iso[11:16]
                    
                    # Ajustement heure +1h et report au lendemain si minuit
                    date_str, time_str = get_adjusted_datetime(date_str_raw, raw_time, 1)

                    event_id = event.get('id', f"nba_{date_str}_{i}")
                    if event_id not in seen_ids:
                        seen_ids.add(event_id)
                        
                        status_type = event.get('status', {}).get('type', {})
                        status_state = status_type.get('state', 'pre')
                        is_live = (status_state == 'in')
                        is_finished = (status_state == 'post')

                        venue = competition.get('venue')
                        if venue and venue.get('fullName'):
                            v_name = venue.get('fullName')
                            addr = venue.get('address', {})
                            v_city = addr.get('city', '')
                            v_country = addr.get('country', 'États-Unis')
                            venue_info = f"{v_name} ({v_city} - {v_country})" if v_city else f"{v_name} ({v_country})"
                        else:
                            venue_info = "TBD"

                        competitors = competition['competitors']
                        team1 = competitors[0]
                        team2 = competitors[1]
                        
                        t1_name = team1['team'].get('displayName', 'TBD')
                        t2_name = team2['team'].get('displayName', 'TBD')
                        is_tbd = (t1_name == 'TBD' or t2_name == 'TBD')

                        score_str = ""
                        if is_live or is_finished:
                            s1 = team1.get('score', '0')
                            s2 = team2.get('score', '0')
                            score_str = f"{s1} - {s2}"

                        season_type = event.get('season', {}).get('type', 2)
                        nature_str = "Play-offs NBA" if season_type == 3 else "Saison Régulière"

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
                            "nature": nature_str,
                            "isLive": is_live,
                            "isFinished": is_finished,
                            "score": score_str,
                            "channels": ["beinsports", "dazn"]
                        })
        except Exception as e:
            print(f"Erreur NBA mois {month_str} : {e}")
            
    return events

def main():
    f1_events = fetch_f1_calendar()
    nfl_events = fetch_espn_games("football/nfl", "nfl", [(2, 19, 18), (3, 5, 4)])
    nba_events = fetch_nba_calendar()
    
    all_events = f1_events + nfl_events + nba_events
    all_events.sort(key=lambda x: (x['date'], x['time']))
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
