import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server (Render o'chib qolmasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Bot sozlamalari
TOKEN = "8658483861:AAHXsWeW8xrSfVtiB212cvS5kWtzYuc1z8k"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🔍 Musiqa qidirish")
    item2 = types.KeyboardButton("ℹ️ Yordam")
    markup.add(item1, item2)
    bot.send_message(m.chat.id, "🌟 **X-SONIC Music** botiga xush kelibsiz!\n\nPastdagi tugmani bosing yoki musiqa nomini yozing:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🔍 Musiqa qidirish")
def search_hint(m):
    bot.send_message(m.chat.id, "🎵 Musiqa nomini yoki ijrochini yozing:")

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
    try:
        query = inline_query.query
        # Inline natija oynasi
        r = types.InlineQueryResultArticle(
            id='1',
            title=f"🎵 '{query}' musiqasini qidirish",
            description="Musiqalarni ko'rish uchun bosing",
            input_message_content=types.InputTextMessageContent(
                message_text=f"🔍 **{query}** musiqasi qidirilmoqda..."
            ),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🎧 Musiqani tanlash", switch_inline_query_current_chat=query)
            )
        )
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception as e:
        print(f"Inline xatosi: {e}")

@bot.message_handler(func=lambda m: True)
def handle_text(m):
    query = m.text
    msg = f"🔍 **'{query}'** uchun musiqalar topildi!\n\nEshitish uchun pastdagi tugmani bosing:"
    
    markup = types.InlineKeyboardMarkup()
    # Bu tugma bosilganda @bot nomi va so'z avtomatik yoziladi
    btn = types.InlineKeyboardButton(text="🎵 Musiqalarni ko'rish", switch_inline_query_current_chat=query)
    markup.add(btn)
    
    bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# Botni ishga tushirish (Hamma handlerlardan keyin bo'lishi shart!)
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
