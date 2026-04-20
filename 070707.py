from db_manager import user_saqlash
import telebot, os, yt_dlp, time, re
import database
from telebot import types

# 🔑 To'g'ri tokenni shu yerga qo'ying
TOKEN = "8658483861:AAHXsWeW8xrSfVtiB212cvS5kWtzYuc1z8k"
bot = telebot.TeleBot(TOKEN, threaded=True)

database.init_db()


def clean_name(text):
    return re.sub(r'[^\w\s-]', '', text).strip()


@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"), types.KeyboardButton("ℹ️ Yordam"))
    bot.send_message(m.chat.id, "🌟 **X-SOS Music botiga xush kelibsiz!**", reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda m: True)
def handle_text(m):
    if m.text == "🔍 Musiqa qidirish":
        return bot.send_message(m.chat.id, "🎵 Musiqa nomini yozing:")

    query = m.text
    m_wait = bot.send_message(m.chat.id, "🔎 Qidirilmoqda...")

    try:
        # YouTube-dan 10 ta natija olish
        ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extract': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch10:{query}", download=False)['entries']

        # 2 qatorli chiroyli Inline tugmalar
        markup = types.InlineKeyboardMarkup(row_width=5)
        btns = [types.InlineKeyboardButton(text=str(i + 1), callback_data=f"dl_{v['id']}") for i, v in
                enumerate(results)]
        markup.add(*btns)

        # Sahifalash tugmalari (Dekoratsiya)
        markup.row(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="none"),
                   types.InlineKeyboardButton("Keyingisi ➡️", callback_data="none"))

        res_text = f"🎧 **'{query}' uchun natijalar:**\n\n"
        for i, v in enumerate(results, 1):
            res_text += f"{i}. {v['title'][:50]}...\n"

        bot.delete_message(m.chat.id, m_wait.message_id)
        bot.send_message(m.chat.id, res_text, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.edit_message_text("❌ Hech narsa topilmadi.", m.chat.id, m_wait.message_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('dl_'))
def download(c):
    vid_id = c.data.split('_')[1]
    bot.answer_callback_query(c.id, "📥 Tayyorlanmoqda...")

    # Tezlik uchun bazani tekshiramiz
    cached = database.check_song(vid_id)
    if cached:
        return bot.send_audio(c.message.chat.id, cached[0], title=cached[1], performer="X-SOS")

    msg = bot.send_message(c.message.chat.id, "📥 Yuklanmoqda...")
    try:
        # Fayl nomi xato bermasligi uchun unikal nom
        path = f"downloads/mus_{int(time.time())}.mp3"
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': path, 'quiet': True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=True)
            title = clean_name(info['title'])
            file_on_disk = ydl.prepare_filename(info)

        with open(file_on_disk, 'rb') as f:
            sent = bot.send_audio(c.message.chat.id, f, title=title, performer="X-SOS")
            database.save_song(vid_id, sent.audio.file_id, title)

        os.remove(file_on_disk)
        bot.delete_message(c.message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ Yuklab bo'lmadi.", c.message.chat.id, msg.message_id)


if __name__ == "__main__":
    if not os.path.exists('downloads'): os.makedirs('downloads')
    print("🚀 BOT ISHLASHGA TAYYOR!")
    bot.infinity_polling()