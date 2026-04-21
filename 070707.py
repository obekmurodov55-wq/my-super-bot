import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

TOKEN = "8658483861:AAGwC23u5bGRViLCXeemby8I_q-oz5SPB5c"
bot = telebot.TeleBot(TOKEN)

# 1. INLINE HANDLER - BU QIDIRUV OYNASINI TO'LDIRADI
@bot.inline_handler(lambda query: True) # Har qanday yozuvga javob beradi
def query_text(inline_query):
    try:
        q = inline_query.query if inline_query.query else "musiqa"
        
        # Natija oynasida chiqadigan narsa
        result = types.InlineQueryResultArticle(
            id='1',
            title=f"🎵 '{q}' musiqasini yuklash",
            description="Barcha musiqalarni ko'rish va tanlash uchun bosing",
            thumb_url="https://repost.uz/storage/uploads/95-1610453302-music-db-entry.jpg",
            input_message_content=types.InputTextMessageContent(
                message_text=f"🔍 **{q}** musiqasi qidirilmoqda...\n\nPastdagi tugma orqali musiqani tanlang:"
            ),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🎧 Musiqani tanlash", url=f"https://t.me/vkmusic_bot?start={q}")
            )
        )
        
        # Natijani darrov yuboramiz
        bot.answer_inline_query(inline_query.id, [result], cache_time=1)
    except Exception as e:
        print(f"Inline xato: {e}")

# 2. START BUYRUG'I
@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Musiqa qidirish")
    bot.send_message(m.chat.id, "🌟 **X-SONIC Music**\n\nMusiqa nomini yozing:", reply_markup=markup, parse_mode="Markdown")

# 3. ODDIY XABARLAR
@bot.message_handler(func=lambda m: True)
def handle_text(m):
    query = m.text
    markup = types.InlineKeyboardMarkup()
    # switch_inline_query_current_chat o'rniga switch_inline_query ishlatamiz (xato bermasligi uchun)
    btn = types.InlineKeyboardButton(text="🎵 Musiqalarni ko'rish", switch_inline_query=query)
    markup.add(btn)
    bot.send_message(m.chat.id, f"🔍 **'{query}'** uchun qidiruv tayyor!", reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
