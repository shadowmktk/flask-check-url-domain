from celery import shared_task
from validators import domain as is_domain
from validators import ip_address
from OpenSSL import crypto
from datetime import datetime
from pytz import timezone
import ssl

def load_certificate_date(date_string: str):
    utc = timezone("UTC")
    shanghai = timezone("Asia/Shanghai")
    format_date = datetime.strptime(date_string, "%Y%m%d%H%M%SZ")
    new_date = utc.localize(format_date)
    return new_date.astimezone(tz=shanghai)

class GetCertificateDate(object):
    def __init__(self, certificate: str):
        self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
        
    def get_begin_date(self):
        self.begin_date = load_certificate_date(self.cert.get_notBefore().decode("utf-8"))
        self.begin_date = self.begin_date.strftime("%Y-%m-%d %H:%M:%S")
        return self.begin_date

    def get_expire_date(self):
        self.expire_date = load_certificate_date(self.cert.get_notAfter().decode("utf-8"))
        self.expire_date = self.expire_date.strftime("%Y-%m-%d %H:%M:%S")
        return self.expire_date

    def has_expired(self):
        return self.cert.has_expired()

def check_is_domain(domain):
    if is_domain(domain):
        return True

def check_is_ip_address(ip):
    if ip_address.ipv4(ip):
        return True

@shared_task(name="check_domain_certificate")
def check_domain_certificate(domain, port):
    try:
        if not check_is_domain(domain) and not check_is_ip_address(domain):
            return {
                "domain": domain,
                "error": "域名不正确"
            }
        certificate = ssl.get_server_certificate((domain, port), timeout=3)
        result = GetCertificateDate(certificate)
        to_dict = {
            "域名": domain,
            "证书创建时间": result.get_begin_date(),
            "证书到期时间": result.get_expire_date(),
            "证书是否过期": result.has_expired()
        }
        return to_dict
    except ConnectionError as e:
        return {
                "domain": domain,
                "port": port,
                "error": "请检查domain或port参数是否正确"
            }
    except OSError as e:
        return {
                "domain": domain,
                "domain": port,
                "error": "请检查domain或port参数是否正确"
            }
    except Exception as e:
        return {
                "domain": domain,
                "port": port,
                "error": "请求出错了"
            }