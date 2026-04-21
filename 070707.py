import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. Flask server (Render o'chib qolmasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# 2. Bot sozlamalari
TOKEN = "8658483861:AAHXsWeW8xrSfVtiB212cvS5kWtzYuc1z8k"
bot = telebot.TeleBot(TOKEN)

# 3. Start buyrug'i
@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🔍 Musiqa qidirish")
    item2 = types.KeyboardButton("ℹ️ Yordam")
    markup.add(item1, item2)
    bot.send_message(m.chat.id, "🌟 **X-SOS Music** botiga xush kelibsiz!\n\nMusiqa nomini yozing:", reply_markup=markup, parse_mode="Markdown")

# 4. Musiqa qidirish tugmasi bosilganda
@bot.message_handler(func=lambda m: m.text == "🔍 Musiqa qidirish")
def search_hint(m):
    bot.send_message(m.chat.id, "🎵 Musiqa nomini yozing:")

# 5. INLINE HANDLER (Bu eng muhim qism, qidiruv natijasini chiqaradi)
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
    try:
        q = inline_query.query
        # Bu yerda foydalanuvchi yozgan so'z bo'yicha natija chiqadi
        result = types.InlineQueryResultArticle(
            id='1',
            title=f"🎵 '{q}' musiqasini yuklash",
            description="Barcha musiqalarni ko'rish uchun bosing",
            input_message_content=types.InputTextMessageContent(
                message_text=f"🔍 **{q}** musiqasi qidirilmoqda..."
            ),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🎧 Musiqani tanlash", switch_inline_query_current_chat=q)
            )
        )
        bot.answer_inline_query(inline_query.id, [result], cache_time=1)
    except Exception as e:
        print(f"Xato: {e}")

# 6. Har qanday matn yozilganda tugma chiqarish
@bot.message_handler(func=lambda m: True)
def handle_text(m):
    query = m.text
    markup = types.InlineKeyboardMarkup()
    # Bu tugma Inline rejimni uyg'otadi
    btn = types.InlineKeyboardButton(text="🎵 Musiqalarni ko'rish", switch_inline_query_current_chat=query)
    markup.add(btn)
    bot.send_message(m.chat.id, f"🔍 **'{query}'** uchun qidiruv tayyor!", reply_markup=markup, parse_mode="Markdown")

# 7. Botni ishga tushirish (FAQAT HAMMA HANDLERLARDAN KEYIN!)
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
