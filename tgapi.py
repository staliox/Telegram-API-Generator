import json
import requests
from lxml import html
from fake_useragent import FakeUserAgent

fake_useragent = FakeUserAgent()

class TelegramApplication:
    def __init__(self,
            phone_number: str,
            app_title: str = "",
            app_shortname: str = "",
            app_url: str = "",
            app_platform: str = "desktop",
            app_desc: str = "",
            random_hash: str = None,
            stel_token: str = None,
            useragent: str = fake_useragent.random
        ) -> None:
        self.phone_number = phone_number
        self.app_title = app_title
        self.app_shortname = app_shortname
        self.app_url = app_url
        self.app_platform = app_platform
        self.app_desc = app_desc
        self.random_hash = random_hash
        self.stel_token = stel_token
        self.useragent = useragent
    
    def send_password(self) -> bool:
        try:
            response = requests.post(
                url="https://my.telegram.org/auth/send_password",
                data="phone={0}".format(self.phone_number),
                headers={
                    "Origin": "https://my.telegram.org",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                    "User-Agent": self.useragent,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Reffer": "https://my.telegram.org/auth",
                    "X-Requested-With": "XMLHttpRequest",
                    "Connection": "keep-alive",
                    "Dnt": "1"
                })
            
            get_json = json.loads(response.content)
            self.random_hash = get_json["random_hash"]
            return True
        except:
            return False

    def auth_login(self, cloud_password: str) -> bool:
        try:
            responses = requests.post(
                url="https://my.telegram.org/auth/login",
                data="phone={0}&random_hash={1}&password={2}".format(self.phone_number, self.random_hash, cloud_password),
                headers={
                    "Origin": "https://my.telegram.org",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                    "User-Agent": self.useragent,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Reffer": "https://my.telegram.org/auth",
                    "X-Requested-With": "XMLHttpRequest",
                    "Connection": "keep-alive",
                    "Dnt": "1"
                }
            )
            self.stel_token = responses.cookies['stel_token']
            return True
        except:
            return False

    def auth_app(self) -> tuple:
        try:
            resp = requests.get(
                url="https://my.telegram.org/apps",
                headers={
                    "Cookie": "stel_token={0}".format(self.stel_token),
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": self.useragent,
                    "Reffer": "https://my.telegram.org/org",
                    "Cache-Control": "max-age=0",
                    "Dnt": "1"
                }
            )
            tree = html.fromstring(resp.content)
            api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
            return api[0], api[1]
        except:
            try:
                s = resp.text.split('"/>')[0]
                value = s.split('<input type="hidden" name="hash" value="')[1]
                
                requests.post(
                    url="https://my.telegram.org/apps/create",
                    data="hash={0}&app_title={1}&app_shortname={2}&app_url={3}&app_platform={4}&app_desc={5}".format(value, self.app_title, self.app_shortname, self.app_url, self.app_platform, self.app_desc),
                    headers={
                        "Cookie": "stel_token={0}".format(self.stel_token),
                        "Origin": "https://my.telegram.org",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                        "User-Agent": self.useragent,
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Accept": "*/*",
                        "Referer": "https://my.telegram.org/apps",
                        "X-Requested-With": "XMLHttpRequest",
                        "Connection": "keep-alive",
                        "Dnt":"1"
                    }
                )
                
                
                response = requests.get(
                    url="https://my.telegram.org/apps",
                    headers={
                        "Cookie": "stel_token={0}".format(self.stel_token),
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": self.useragent,
                        "Reffer": "https://my.telegram.org/org",
                        "Cache-Control": "max-age=0",
                        "Dnt":"1"
                    }
                )
                trees = html.fromstring(response.content)
                api = trees.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
                return api[0], api[1]
            except:
                return False
