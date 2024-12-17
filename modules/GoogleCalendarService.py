import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleCalendarService:

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    TOKEN_PATH = 'token.json'
    CREDENTIALS_PATH = 'credentials.json'

    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists(self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_PATH, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    def add_to_google_calendar(self, summary, location, description, start_date,
                               end_date, time_zone='Europe/Bratislava'):
        """
        Add event to Google calendar
        :param summary: Name of the event
        :param location: Place of the event
        :param description: Event description
        :param start_date: Start of the event (YYYY-MM-DD)
        :param end_date: End of the event (YYYY-MM-DD)
        :param time_zone: Time zone
        """
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {'date': start_date, 'timeZone': time_zone},
            'end': {'date': end_date, 'timeZone': time_zone},
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f"Udalosť bola vytvorená: {created_event.get('htmlLink')}")
        return created_event['id']

    def update_event(self, event_id, updated_data):
        """
        Update event in Google calendar
        :param event_id: ID of the event
        :param updated_data: Updated data
        """
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        event.update(updated_data)
        updated_event = self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        print(f"Udalosť bola aktualizovaná: {updated_event.get('htmlLink')}")

    def delete_event(self, event_id):
        """
        Delete event in Google calendar
        :param event_id: ID of the event
        """
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Udalosť s ID {event_id} bola úspešne zrušená.")

    def list_events(self, max_results=10):
        """
        Get list of upcoming events and their IDs
        :param max_results: Max number of listed events
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Získavam nadchádzajúce udalosti...')
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now, maxResults=max_results,
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('Žiadne nadchádzajúce udalosti.')
            return

        print('Nadchádzajúce udalosti:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"ID: {event['id']} | Začiatok: {start} | Názov: {event['summary']}")


if __name__ == '__main__':
    # Proklad pouzitia
    calendar_service = GoogleCalendarService()

    # Pridanie udalosti
    # event_id = calendar_service.add_to_google_calendar(
    #     summary='Príklad udalosti',
    #     location='Bratislava',
    #     description='Popis novej udalosti pre Google Kalendár',
    #     start_date='2024-12-18',
    #     end_date='2024-12-19'
    # )

    # Aktualizacia udalosti
    # calendar_service.update_event('hgh2isjaebmrkfsh0ge130nkf4', {'summary': 'Aktualizovaný názov udalosti'})

    # Zrusenie udalosti
    # calendar_service.delete_event('hgh2isjaebmrkfsh0ge130nkf4')

    # Zoznam nadchadzajucich udalosti
    # calendar_service.list_events()
