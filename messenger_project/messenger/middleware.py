import logging
import time

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from messenger.models import UserStatus

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


class UpdateLastActivityMiddleware:
    """Мідлвеє для оновлення останньої активності користувача."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            UserStatus.objects.update_or_create(
                user=request.user,
                defaults={'last_activity': timezone.now()}
            )
        return response
