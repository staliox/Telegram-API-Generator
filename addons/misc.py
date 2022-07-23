from datetime import datetime
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup()
main_keyboard.row(InlineKeyboardButton(text='🔖 Get API', callback_data='api'))
main_keyboard.row(InlineKeyboardButton(text='🌀 Channel', url='https://t.me/V1llN'), InlineKeyboardButton(text='🖥 Developer', url='https://t.me/Staliox'))

cancel_keyboard = InlineKeyboardMarkup()
cancel_keyboard.row(InlineKeyboardButton(text='🔙', callback_data='cancel'))

join_keyboard = InlineKeyboardMarkup()
join_keyboard.row(InlineKeyboardButton(text='🌀 Channel', url='https://t.me/V1llN'))

def timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return round(timestamp)

md_symbols = {
    "*" : "\*",
    "_" : "\_",
    "`" : "\`"
}
    
def replace_md(text: str) -> str:
    for i, j in md_symbols.items():
        text = text.replace(i, j)
    return text

async def is_join_member(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        user = await bot.get_chat_member(chat_id, user_id)
        return user.status != "left"
    except:
        pass