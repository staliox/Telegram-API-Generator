API_ID = 0000000
API_HASH = "XXXXXXXXXXXXXXXXXXXXXXX"
BOT_TOKEN = "0000000:XXXXXXXXXXXXXXXXXXXXXXXXX"

import json, requests
from lxml import html
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from pyromod import listen

class TelegramApplication:
    def send_cloud_password(self, phone):
        try:
            response = requests.post("https://my.telegram.org/auth/send_password", data=f"phone={phone}", headers={"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
            get_json = json.loads(response.content)
            return get_json["random_hash"]
        except:
            return False

    def auth(self, phone, hash_code, cloud_password):
        responses = requests.post('https://my.telegram.org/auth/login', data=f"phone={phone}&random_hash={hash_code}&password={cloud_password}", headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
        try:
            return responses.cookies['stel_token']
        except:
            return False

    def auth_app(self, stel_token):
        resp = requests.get('https://my.telegram.org/apps', headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":f"stel_token={stel_token}" ,"Cache-Control": "max-age=0",})
        tree = html.fromstring(resp.content)
        api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
        try:
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
        
telegram_application = TelegramApplication()
app = Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
        
main_keyboard = ReplyKeyboardMarkup(
    [
        ['《 Get API ID & API Hash 》', '《 Help 》'],
        ['《 Creator 》']
    ],
    resize_keyboard=True
)
        
cancel_keyboard = ReplyKeyboardMarkup(
    [
        ['《 Cancel 》']
    ],
    resize_keyboard=True
)

@app.on_message(filters.private & (filters.text | filters.contact))
async def message_handler(_, message: Message):
    text = message.text or ""
    
    if text.lower() == "/start":
        await message.reply(f'🖥 Hi {message.from_user.first_name}\n🖥 Choose an option to continue!', reply_markup=main_keyboard, quote=True)
    
    elif text.lower() == "《 help 》":
        await message.reply("📰 This a bot that help you to create or get 'API ID' & 'API Hash' from my telegram, Just click on 'Get API ID & API Hash' then send your phone number or share your phone number, You will get a code from telegram, Forward or copy that message or just send code here to create or get informations!", reply_markup=main_keyboard, quote=True)
    
    elif text.lower() == "《 creator 》":
        await message.reply("📰 @Staliox", reply_markup=main_keyboard, quote=True)
    
    elif text.lower() == "《 get api id & api hash 》":
        get_phone = await app.ask(message.chat.id, "⚙️ Send your phone number or share your phone number:", reply_markup=cancel_keyboard, reply_to_message_id=message.message_id or 0, filters=filters.text | filters.contact)
        
        if get_phone.contact:
            phone_number = get_phone.contact.phone_number
        else:
            phone_number = get_phone.text
        
        if phone_number == "《 cancel 》":
            await message.reply(f'🖥 Hi {message.from_user.first_name}\n🖥 Choose an option to continue!', reply_markup=main_keyboard, quote=False)
        else:
            phone_number = phone_number.replace(" ", "")
            hash = telegram_application.send_cloud_password(phone_number)
            if hash:
                get_code = await app.ask(message.chat.id, "⚙️ Forward or copy that message or just send code here:", reply_markup=cancel_keyboard, reply_to_message_id=message.message_id or 0, filters=filters.text)
                if get_code.text.lower() == "《 cancel 》":
                    await message.reply(f'🖥 Hi {message.from_user.first_name}\n🖥 Choose an option to continue!', reply_markup=main_keyboard)
                else:
                    if get_code.text.startswith("Web login code"):
                        cloud_password = get_code.text.split('\n')[1]
                    else:
                        cloud_password = get_code.text
                    token = telegram_application.auth(phone_number, hash, cloud_password)
                    if token:
                        api = telegram_application.auth_app(token)
                        if api:
                            await message.reply(f"🔖 Phone Number: `{phone_number}`\n🔖 API ID: `{api[0]}`\n🔖 API HASH: `{api[1]}`\n📰 Creator: @Staliox", reply_markup=main_keyboard)
                        else:
                            await message.reply("⚙️ Cannot get data from telegram!", reply_markup=main_keyboard)
                    else:
                        await message.reply("⚙️ Code is invalid!", reply_markup=main_keyboard)
            else:
                await message.reply("⚙️ Cannot send code to this number!", reply_markup=main_keyboard)

if __name__ == '__main__':
    app.run()
