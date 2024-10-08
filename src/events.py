from datetime import datetime, timedelta

import requests
from requests import Response


def get_json_data(url: str) -> list[dict[str]]:
    response: Response = requests.get(url)
    if response.status_code == 200:
        data: list[dict[str]] = response.json()  # Parse JSON data
        return data
    print('Failed to retrieve data:', response.status_code)
    return []


def get_weekly_events(event_list: list[dict[str]]) -> list[dict[str]]:
    weekly_events: list[dict[str]] = []
    current_date: datetime = datetime.now()
    end_date: datetime = current_date + timedelta(days=1)

    for event in event_list:
        event_date: datetime = datetime.strptime(event.get('date_utc', '').split(' ')[0], '%Y-%m-%d')
        if current_date <= event_date < end_date:
            weekly_events.append(event)

    return weekly_events


def get_event_data(event: dict) -> str:
    try:
        event_title: str = event.get('title')
        event_date_formatted: str = event.get('date')
        event_url: str = event.get('url')
        event_information = (f'>>> ## Event Title: {event_title}\n'
                             f'Event Date: ``{event_date_formatted}``\n'
                             f'Event URL: [**{event_title}**]({event_url})')
        return event_information
    except Exception as e:
        print('Failed to retrieve data:', e)
    return 'No Information Found'
