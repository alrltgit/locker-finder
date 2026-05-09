import requests

def handle_runtime_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            raise RuntimeError(f"InPost API error: {e}")
    return wrapper