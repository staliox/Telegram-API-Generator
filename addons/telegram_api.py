import json
import requests
from lxml import html

class TelegramApplication:
    def send_cloud_password(self, phone):
        try:
            response = requests.post("https://my.telegram.org/auth/send_password", data=f"phone={phone}", headers={"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
            get_json = json.loads(response.content)
            return get_json["random_hash"]
        except:
            return False

    def auth(self, phone, hash_code, cloud_password):
        try:
            responses = requests.post('https://my.telegram.org/auth/login', data=f"phone={phone}&random_hash={hash_code}&password={cloud_password}", headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
            return responses.cookies['stel_token']
        except:
            return False

    def auth_app(self, stel_token):
        try:
            resp = requests.get('https://my.telegram.org/apps', headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":f"stel_token={stel_token}" ,"Cache-Control": "max-age=0",})
            tree = html.fromstring(resp.content)
            api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
            return api[0], api[1]
        except:
            try:
                s = resp.text.split('"/>')[0]
                value = s.split('<input type="hidden" name="hash" value="')[1]
                requests.post('https://my.telegram.org/apps/create', data=f"hash={value}&app_title=Telegram Android&app_shortname=Telegram Android&app_url=&app_platform=desktop&app_desc=",headers={"Cookie":"stel_token={0}".format(stel_token),"Origin": "https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*","Referer": "https://my.telegram.org/apps","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
                respv = requests.get('https://my.telegram.org/apps', headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":f"stel_token={stel_token}", "Cache-Control": "max-age=0",})
                trees = html.fromstring(respv.content)
                api = trees.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
                return api[0], api[1]
            except:
                return False