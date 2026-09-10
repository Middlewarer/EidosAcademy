from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        cache.set("healthcheck", "ok", timeout=10)
        if cache.get("healthcheck") != "ok":
            raise RuntimeError("Cache is unavailable")
    except Exception:
        return JsonResponse({"status": "unavailable"}, status=503)

    return JsonResponse({"status": "ok"})
