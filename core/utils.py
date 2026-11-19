"""Helpers that let the project run with or without PostgreSQL / Redis / Celery."""
import operator
import threading
import time
from functools import reduce

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.models import Q


# ---------------------------------------------------------------- cache TTL
def cache_set(key, value, timeout):
    """cache.set() that also remembers when the key expires, so ttl() works on any backend."""
    cache.set(key, value, timeout=timeout)
    cache.set(f'{key}__expires_at', time.time() + timeout, timeout=timeout)


def cache_ttl(key):
    """Seconds left before `key` expires. Returns -2 when it is missing (same as Redis TTL)."""
    expires_at = cache.get(f'{key}__expires_at')
    if expires_at is None or cache.get(key) is None:
        return -2
    return max(int(expires_at - time.time()), 0)


# ---------------------------------------------------------------- tasks
def run_later(task, args=(), countdown=0):
    """task.apply_async(countdown=...) when Celery is running; otherwise a background timer."""
    if getattr(settings, 'USE_CELERY', False):
        return task.apply_async(args=list(args), countdown=countdown)
    timer = threading.Timer(countdown, _safe_call, args=(task, args))
    timer.daemon = True
    timer.start()
    return timer


def _safe_call(task, args):
    try:
        task(*args)
    except Exception as exc:  # never crash the timer thread
        print(f'[background task {getattr(task, "name", task)}] {exc}')


# ---------------------------------------------------------------- search
def text_search(queryset, fields, query):
    """PostgreSQL full-text search when available, else a case-insensitive word match."""
    if not query:
        return queryset.none()
    if connection.vendor == 'postgresql':
        from django.contrib.postgres.search import SearchVector
        return queryset.annotate(search=SearchVector(*fields)).filter(search=query).order_by('-search')

    words = [w for w in query.replace(',', ' ').split() if w]
    conditions = [
        reduce(operator.or_, (Q(**{f'{field}__icontains': word}) for field in fields))
        for word in words
    ]
    return queryset.filter(reduce(operator.and_, conditions)).distinct().order_by('-pk')
