import logging
import time
from threading import local


thread_locals = local()


logger = logging.getLogger(__name__)


class RequestLogger:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        thread_locals.path = request.path # текущий path
        thread_locals.sql_count = 0 # количество SQL запросов
        thread_locals.sql_total = 0 # общая продолжительность SQL запросов
        timestamp = time.monotonic()
        response = self.get_response(request)
        logger.info( # выводим информацию через logger.info, также есть разные уровни который описывает серьезность сообщений, в данном случае это общая информация
            f"Метод - {request.method} Путь - {request.path} Пользователь - {request.user.username}\n" # вывод: метод и путь запроса, имя пользователя 
            f'Время запроса={time.monotonic() - timestamp:.3f} сек.\n'
            f'Количество SQL-запросов - {thread_locals.sql_count}.\n'
            f'Продолжительность SQL-запросов - {thread_locals.sql_total:.3f}.\n'
            )
        
        thread_locals.sql_total = 0 # пустое значение после выполнения
        thread_locals.sql_count = 0 # пустое значение после выполнения
        thread_locals.path = '' # пустое значение после выполнения
        return response
