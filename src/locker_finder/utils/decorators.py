import requests

def handle_runtime_error(message="An error occurred"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                raise RuntimeError(f"{message}: {e}")
        return wrapper
    return decorator