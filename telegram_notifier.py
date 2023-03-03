import requests
from datetime import datetime
import pytz
import os


CB_TIME_ZONE = pytz.timezone('Africa/Casablanca')
RAW_TIME_ZONE = datetime.now(CB_TIME_ZONE)

TELEGRAM_API_TOKEN = os.environ.get("DB_TELEGRAM_API_TOKEN_JOB_OFFERS_NOTIFIER")
TELEGRAM_GROUP_ID = os.environ.get("DB_JOB_OFFERS_TELEGRAM_GROUP_ID")
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/'


class TelegramNotifier:
    def __init__(self):
        self.current_date = self._get_current_date()
        self.current_time = self._get_current_time()

    @staticmethod
    def publish(texts):
        # Create a session object
        session = requests.Session()
        # Loop through each text
        for text in texts:
            # Get the text ready to send
            text_to_send = text
            # Ready the URL
            url = f'{TELEGRAM_API_URL}sendMessage?chat_id=@{TELEGRAM_GROUP_ID}&text={text_to_send}'
            # Send a get request to the Telegram message API url
            response = session.get(url)
            if response.status_code == 200:
                print('Message was successfully sent')
            else:
                print('Message was not sent.')

    @staticmethod
    def _get_current_date():
        return RAW_TIME_ZONE.strftime("%d/%m/%Y")

    @staticmethod
    def _get_current_time():
        return RAW_TIME_ZONE.strftime("%H:%M:%S")

