import time
import uuid

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse

LIMIT = 50      # requests
WINDOW = 60     # seconds


class RateLimiting:
    """Sliding-window rate limiter. Uses a Redis sorted set when Redis is configured,
    otherwise a list of timestamps in the Django cache."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_conn = None
        if getattr(settings, 'USE_CELERY', False):
            from django_redis import get_redis_connection
            self.redis_conn = get_redis_connection("default")

    def _count(self, key, now):
        if self.redis_conn is not None:
            self.redis_conn.zremrangebyscore(key, 0, now - WINDOW)
            count = self.redis_conn.zcard(key)
            self.redis_conn.zadd(key, {str(uuid.uuid4()): now})
            self.redis_conn.expire(key, WINDOW)
            return count
        cache_key = f'ratelimit:{key}'
        hits = [t for t in cache.get(cache_key, []) if t > now - WINDOW]
        count = len(hits)
        hits.append(now)
        cache.set(cache_key, hits, timeout=WINDOW)
        return count

    def __call__(self, request):
        if request.path.startswith(settings.STATIC_URL if settings.STATIC_URL.startswith('/') else '/' + settings.STATIC_URL):
            return self.get_response(request)
        key = f'user:{request.user.id}' if request.user.is_authenticated else f'ip:{request.META.get("REMOTE_ADDR")}'
        if self._count(key, time.time()) + 1 > LIMIT:
            return HttpResponse('Rate Limit', status=429)
        return self.get_response(request)


class JobLifecycleFallback:
    """When Celery beat is not running, run the daily job-lifecycle tasks
    (close applications after deadline, terminate expired jobs) at most once an hour."""

    INTERVAL = 60 * 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, 'USE_CELERY', False) and cache.add('job-lifecycle-ran', True, self.INTERVAL):
            from jobs.tasks import close_applications, terminate_jobs
            try:
                close_applications()
                terminate_jobs()
            except Exception as exc:
                print(f'[job lifecycle] {exc}')
        return self.get_response(request)
