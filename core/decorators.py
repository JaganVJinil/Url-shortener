# core/decorators.py
from functools import wraps
from django.utils.cache import patch_cache_control

def no_cache(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if response is not None:
            patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
        return response
    return _wrapped_view
