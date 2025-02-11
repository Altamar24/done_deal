import logging
import time


logger = logging.getLogger(__name__)


class RequestLogger:

    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        timestamp = time.monotonic()
        response = self.get_response(request)
 
        logger.info(
            f"Метод={request.method} Путь={request.path} Пользователь={request.user.username}\n"
            f'Время запроса={time.monotonic() - timestamp:.3f} сек.'
            )
        return response
