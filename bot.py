
import os
import telebot
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
HF_TOKEN = os.environ["HF_TOKEN"]

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "أهلاً! 🎨 ابعتلي وصف الصورة اللي عايزها.")

@bot.message_handler(func=lambda m: True)
def generate(message):
    bot.reply_to(message, "جاري إنشاء الصورة، انتظر قليلاً...")
    try:
        url = "https://router.huggingface.co/v1/images/generations"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": message.text
        }
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        from io import BytesIO
        bot.send_photo(message.chat.id, BytesIO(r.content))
    except Exception:
        bot.reply_to(message, "تعذر إنشاء الصورة. حاول مرة أخرى.")

bot.infinity_polling()

