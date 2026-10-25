def fetch_nba_calendar():
    events = []
    seen_ids = set()
    today_str = datetime.now().strftime('%Y-%m-%d')
    nba_logo = "https://a.espncdn.com/i/teamlogos/leagues/500/nba.png"
    
    # 2 = Saison régulière, 3 = Play-offs
    phases = [
        (2, "Saison Régulière"),
        (3, "Play-offs NBA")
    ]
    
    for seasontype, phase_label in phases:
        # On interroge l'API globale de la saison NBA en cours
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=2026-2027&seasontype={seasontype}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                for i, event in enumerate(data.get('events', [])):
                    competition = event['competitions'][0]
                    date_iso = competition['date']
                    date_str = date_iso[:10]
                    
                    if date_str >= today_str:
                        event_id = event.get('id', f"nba_st{seasontype}_{i}")
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
            print(f"Erreur NBA : {e}")
            
    return events
