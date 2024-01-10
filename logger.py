"""
Добавление логов.
"""
from loguru import logger

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG',
           rotation='1 MB', compression='zip')
