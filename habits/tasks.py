from datetime import datetime, timedelta
from pprint import pprint

import requests
from celery import shared_task
import logging

from config import settings
from users.models import User
from habits.models import Habit

logger = logging.getLogger(__name__)
TG_BOT_API_KEY = settings.TG_BOT_API_KEY


@shared_task(name='send_tg_message')
def send_tg_message():
    logger.info('Начало работы рассылки.')
    date = datetime.now().date()
    current_time = datetime.now().time()
    logger.info(f'Время: {current_time}')
    habits = Habit.objects.filter(date=date)
    logger.info(f'Привычки: {habits}')
    for habit in habits:
        if habit.time <= current_time:
            url = (f'https://api.telegram.org/bot{TG_BOT_API_KEY}/'
                   f'sendMessage?chat_id={habit.user.chat_id}&text={habit.habit_text()}')
            response = requests.get(url)
            logger.info(response.json())
            habit.date += timedelta(days=habit.periodicity)
            habit.save()
            logger.info(f'Дата следующей отправки: {habit.date}.')
