from celery import shared_task
from .http_status_code import HTTPStatusCode
from validators import url as is_url
import requests

def check_is_url(url):
    if is_url(url):
        return True

@shared_task(name="check_url_status")
def check_url_status(url):
    try:
        if not check_is_url(url):
            return {
                "url": url,
                "error": "URL不正确"
            }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        rs = requests.request("get", url, headers=headers, timeout=10)
        response = HTTPStatusCode().http_status_code[f"{rs.status_code}"]
        return {
            "url": url, 
            "status": rs.status_code, 
            "data": response
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "url": url, 
            "error": "请求出错了"
        }