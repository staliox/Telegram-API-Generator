import asyncio
import phonenumbers

from time import strftime, gmtime
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ChatType, ContentType

from addons.database import Database
from addons.telegram_api import TelegramApplication
from addons.misc import main_keyboard, cancel_keyboard, join_keyboard, timestamp, replace_md, is_join_member

from config import BOT_TOKEN, CHANNEL_USERNAME

app = Bot(BOT_TOKEN)
dispatcher = Dispatcher(app)

telegram_api = TelegramApplication()
database = Database()
users_hash = dict()
edit_messages = dict()

@dispatcher.message_handler(commands=["start"], content_types=ContentType.TEXT, chat_type=ChatType.PRIVATE)
async def start_handler(message: Message):
    user_id = message.from_user.id
    
    is_join =  await is_join_member(app, f"@{CHANNEL_USERNAME}", user_id)
    if not is_join:
        return await message.reply(f"*🔹 Please join to the channel.*", parse_mode="Markdown", reply_markup=join_keyboard)
    
    get_user = database.get_user(user_id)
    
    if not get_user:
        database.add_user(user_id, timestamp())
    
    send_message = await message.reply("⏳")    
    await asyncio.sleep(2)
    await send_message.edit_text(f'*🔹 Hi {replace_md(message.from_user.full_name)}، Welcome to the API Generator.*', parse_mode="Markdown", reply_markup=main_keyboard)

@dispatcher.message_handler(content_types=[ContentType.TEXT, ContentType.CONTACT], chat_type=ChatType.PRIVATE)
async def msg_handler(message: Message):
    user_id = message.from_user.id
    
    is_join =  await is_join_member(app, f"@{CHANNEL_USERNAME}", user_id)
    if not is_join:
        return await message.reply(f"*🔹 Please join to the channel.*", parse_mode="Markdown", reply_markup=join_keyboard)
    
    text = message.text or ""
    get_user = database.get_user(user_id)
        
    if not get_user:
        database.add_user(user_id, timestamp())
    
    if user_id in edit_messages:
        await edit_messages[user_id].edit_reply_markup(None)
        edit_messages.pop(user_id)
    
    if get_user['step'] == 'get_number':
        if message.contact:
            phone_number = message.contact.phone_number
        else:
            phone_number = text.replace(' ', '')
        
        if phone_number[:1] != "+":
            phone_number = f"+{phone_number}"
        
        valid = False
        try:
            check_number = phonenumbers.parse(phone_number)
            if phonenumbers.is_valid_number(check_number):
                valid = True
        except:
            pass
        
        if not valid:
            edit_messages[user_id] = await message.reply(f'*🔹 Phone number is incorrect.*', parse_mode="Markdown", reply_markup=cancel_keyboard)
            return
        
        database.cursor.execute("SELECT * FROM `limits` WHERE `phone_number` = ?;", (phone_number,))
        result = database.cursor.fetchone()
        if result is not None and result["limit"] > timestamp():
            edit_messages[user_id] = await message.reply(f'*🔹 This phone number is limit until {strftime("%M:%S", gmtime(result["limit"] - timestamp()))}.*', reply_markup=cancel_keyboard)
            return
            
        send_cloud_password = telegram_api.send_cloud_password(phone_number)
        
        if not send_cloud_password:
            edit_messages[user_id] = await message.reply(f'*🔹 The operation encountered an error.*', parse_mode="Markdown", reply_markup=cancel_keyboard)
            return
        
        users_hash[user_id] = list()
        users_hash[user_id].append(phone_number)
        users_hash[user_id].append(send_cloud_password)
        
        database.edit_user(user_id, 'step', 'get_code')
        edit_messages[user_id] = await message.reply(f'*🔹 Please send the code that sent from telegram or forward that message.*', parse_mode="Markdown", reply_markup=cancel_keyboard)
            
    elif get_user['step'] == 'get_code':
        if "Web login code" in message.text:
            cloud_password = message.text.split('\n')[1]
        else:
            cloud_password = message.text
        
        phone_number = users_hash[message.from_user.id][0]
        random_hash = users_hash[message.from_user.id][1]
        
        users_hash.pop(message.from_user.id)
        database.edit_user(user_id, 'step', None)
            
        token = telegram_api.auth(phone_number, random_hash, cloud_password)
        if not token:
            return await message.reply(f'*🔹 Code is incorrect.*', parse_mode="Markdown", reply_markup=main_keyboard)
            
        api = telegram_api.auth_app(token)
        if not api:
            return await message.reply(f'*🔹 The operation encountered an error.*', parse_mode="Markdown", reply_markup=main_keyboard)
        
        database.cursor.execute(f"UPDATE `users` SET `limit` = ? WHERE `user_id` = ?;", (timestamp() + 600, message.from_user.id,))
        database.connection.commit()
                            
        database.cursor.execute("SELECT * FROM `limits` WHERE `phone_number` = ?;", (phone_number,))
        result = database.cursor.fetchone()
        if result is None:
            database.cursor.execute("INSERT INTO `limits` (`phone_number`, `limit`) VALUES (?, ?);", (phone_number, timestamp() + 600,))
            database.connection.commit()
        else:
            database.cursor.execute(f"UPDATE `limits` SET `limit` = ? WHERE `phone_number` = ?;", (timestamp() + 600, phone_number,))
            database.connection.commit()
            
        await message.reply(f"*🌓 Api information for number* `{phone_number}` *is as follows:*\n\n*🌓 API ID:* `{api[0]}`\n*🌓 API HASH:* `{api[1]}`\n\n*🌓 Developed By: @Staliox*", parse_mode="Markdown", reply_markup=main_keyboard)
        
    else:
        await message.reply(f'*🔹 Command is invalid.*', parse_mode="Markdown", reply_markup=main_keyboard)
        
@dispatcher.callback_query_handler()
async def callback_handler(query: CallbackQuery):
    user_id = query.from_user.id
    
    is_join =  await is_join_member(app, f"@{CHANNEL_USERNAME}", user_id)
    if not is_join:
        return await query.answer(f"You aren't in channel @{CHANNEL_USERNAME}.", True)
    
    data = query.data
    get_user = database.get_user(user_id)
    
    if data == "api" and not get_user['step']:
        if get_user['limit'] > timestamp():
            return await query.answer(f'You can\'t use the bot until {strftime("%M:%S", gmtime(get_user["limit"] - timestamp()))}.', True)
            
        database.edit_user(user_id, 'step', 'get_number')
        edit_messages[user_id] = await query.message.edit_text(f'*🔹 Please send or share your phone number.*', parse_mode="Markdown", reply_markup=cancel_keyboard)

    elif data == 'cancel' and get_user['step'] in ['get_number', 'get_code']:
        if user_id in users_hash:
            users_hash.pop(user_id)
        
        database.edit_user(user_id, 'step', None)
        await query.message.edit_text(f'*🔹 Hi {replace_md(query.from_user.full_name)}، Welcome to the Api Generator.*', parse_mode="Markdown", reply_markup=main_keyboard)
    
    else:        
        await query.answer("You can't use this button at the moment.", True)
    
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)