from datetime import datetime, timezone
from typing import List, Dict, Any

def parse_event_duration(start_time_str: str, end_time_str: str) -> float:
    clean_start = start_time_str.replace('Z', '').split('+')[0]
    clean_end = end_time_str.replace('Z', '').split('+')[0]
    
    start_dt = datetime.fromisoformat(clean_start)
    end_dt = datetime.fromisoformat(clean_end)
    duration_seconds = (end_dt - start_dt).total_seconds()
    return round(duration_seconds / 3600, 2)

def calculate_session_earnings(events: List[Dict[str, Any]], course_rates: Dict[str, float]) -> List[Dict[str, Any]]:
    processed_sessions = []
    
    for event in events:
        summary = event.get('summary', 'no title')
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

