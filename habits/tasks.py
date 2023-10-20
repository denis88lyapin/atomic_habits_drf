from datetime import datetime

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
    print(date, TG_BOT_API_KEY)
