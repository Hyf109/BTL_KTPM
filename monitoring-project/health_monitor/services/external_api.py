import requests

def check_external_api(api_url):
    try:
        response = requests.get(api_url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
