import requests

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            raise RuntimeError(f"InPost API error: {e}")
    return wrapper