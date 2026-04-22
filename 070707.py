import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread
import time

# 1. Flask server (Render o'chib qolmasligi uchun "Antivirus")
app = Flask(__name__)

@app.route('/')
def home():
    return "X-SONIC Music Bot is Live!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# 2. Bot sozlamalari
# DIQQAT: Agar xato bersa, BotFather-dan tokenni REVOKE qilib yangisini qo'ying!
TOKEN = "8658483861:AAHXsWeW8xrSfVtiB212cvS5kWtzYuc1z8k"
bot = telebot.TeleBot(TOKEN)

# 3. INLINE HANDLER (Musiqa qidirish oynasi)
@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    try:
        q = inline_query.query if inline_query.query else "Top"
        
        # Qidiruv natijasi sifatida bitta chiroyli karta chiqaramiz
        result = types.InlineQueryResultArticle(
            id='1',
            title=f"🎵 '{q}' uchun musiqalar tayyor!",
            description="Musiqalarni eshitish va yuklash uchun bosing",
            thumb_url="https://repost.uz/storage/uploads/95-1610453302-music-db-entry.jpg",
            input_message_content=types.InputTextMessageContent(
                message_text=f"🔍 **{q}** bo'yicha qidiruv natijalari topildi.\n\nPastdagi tugma orqali musiqalarni tanlashingiz mumkin 👇",
                parse_mode="Markdown"
            ),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🎧 Musiqalarni tanlash", url=f"https://t.me/vkmusic_bot?start={q}")
            )
        )
        bot.answer_inline_query(inline_query.id, [result], cache_time=1)
    except Exception as e:
        print(f"Inline xato: {e}")

# 4. START BUYRUG'I
@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"))
    welcome_text = (
        "🌟 **X-SONIC MUSIC**\n\n"
        "Eng tezkor musiqa qidirish botiga xush kelibsiz!\n"
        "Musiqa nomini yozing yoki tugmani bosing:"
    )
    bot.send_message(m.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# 5. ODDIY MATNLI QIDIRUV
@bot.message_handler(func=lambda m: True)
def handle_all_messages(m):
    query = m.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(m.chat.id, "🎵 Musiqa yoki ijrochi nomini yozing:")
        return

    markup = types.InlineKeyboardMarkup()
    # switch_inline_query tugmasi - bu eng to'g'ri yo'l!
    btn = types.InlineKeyboardButton(text="🎧 Natijalarni ko'rish", switch_inline_query=query)
    markup.add(btn)
    
    bot.send_message(m.chat.id, f"🔍 **'{query}'** qidirilmoqda...", reply_markup=markup, parse_mode="Markdown")

# 6. ASOSIY ISHGA TUSHIRISH QISMI
if __name__ == "__main__":
    # Serverni alohida oqimda yoqamiz
    t = Thread(target=run)
    t.start()
    
    # Conflict 409 xatosini oldini olish uchun kichik pauza va polling
    print("Bot muvaffaqiyatli ishga tushdi...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling xatosi: {e}")
            time.sleep(5) # Xato bo'lsa 5 soniya kutib qayta urinadi
