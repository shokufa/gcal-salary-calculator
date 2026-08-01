import requests
from datetime import datetime
from typing import List, Dict, Any

PISTACHIO_COLOR_ID = "2"  
TOMATO_RED_COLOR_ID = "11"

def parse_event_duration(start_time_str: str, end_time_str: str) -> float:
    clean_start = start_time_str.replace('Z', '').split('+')[0]
    clean_end = end_time_str.replace('Z', '').split('+')[0]
    
    start_dt = datetime.fromisoformat(clean_start)
    end_dt = datetime.fromisoformat(clean_end)
    duration_seconds = (end_dt - start_dt).total_seconds()
    return round(duration_seconds / 3600, 2)

def fetch_google_calendar_events(google_token: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    time_min = f"{start_date}T00:00:00Z"
    time_max = f"{end_date}T23:59:59Z"

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {"Authorization": f"Bearer {google_token}"}
    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": True,
        "orderBy": "startTime"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None

    return response.json().get("items", [])

def calculate_session_earnings(
    events: List[Dict[str, Any]], 
    course_rates: Dict[str, float], 
    only_pistachio: bool = True,
    title_filter: str = None
) -> List[Dict[str, Any]]:
    processed_sessions = []

    for event in events:
        event_color = str(event.get('colorId')) if event.get('colorId') is not None else None

        if only_pistachio:
            if event_color == TOMATO_RED_COLOR_ID:
                continue
                
            if event_color != PISTACHIO_COLOR_ID:
                continue

        summary = event.get('summary', 'no title')

        if title_filter and title_filter.strip().lower() not in summary.lower():
            continue

        start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
        end = event.get('end', {}).get('dateTime') or event.get('end', {}).get('date')
        
        if not start or not end or 'T' not in str(start):
            continue
            
        duration = parse_event_duration(start, end)
        
        matched_rate = 0.0
        for course_name, rate in course_rates.items():
            if course_name.lower() in summary.lower():
                matched_rate = rate
                break
                
        earnings = round(duration * matched_rate, 2)
        
        processed_sessions.append({
            "event_title": summary,
            "event_date": start,
            "duration_hours": duration,
            "hourly_rate": matched_rate,
            "total_earnings": earnings
        })
        
    return processed_sessions