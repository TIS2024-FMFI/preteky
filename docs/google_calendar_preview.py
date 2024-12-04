from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Oprávnenia pre Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    # Overenie prístupu k API
    creds = None
    # Pokúsiť sa načítať token.json (ak už existuje)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Ak neexistuje alebo je neplatný, vykonať OAuth autentifikáciu
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Uložiť nový token pre budúce použitie
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Pripojenie k Google Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Definícia udalosti
    event = {
        'summary': 'Test udalosti',
        'location': 'Bratislava',
        'description': 'Test udalosti description',
        'start': {
            'dateTime': '2024-11-27T14:00:00',
            'timeZone': 'Europe/Bratislava',
        },
        'end': {
            'dateTime': '2024-11-27T15:00:00',
            'timeZone': 'Europe/Bratislava',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    # Vytvorenie udalosti
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Udalosť bola vytvorená: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
