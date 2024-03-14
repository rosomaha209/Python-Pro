import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Зберігаємо час початку обробки запиту."""
        request.start_time = time.time()

    def process_response(self, request, response):
        """Розраховуємо та логуємо час виконання запиту."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"Запит до {request.path} виконано за {duration:.2f} сек.")
            print(f"Запит до {request.path} виконано за {duration:.2f} сек.")
        return response
