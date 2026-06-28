import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
import threading

load_dotenv()

TOKEN = os.getenv("TOKEN")
# Botun girmesini istediğiniz ses kanalının ID'sini buraya yazın
VOICE_CHANNEL_ID = 1519341566282698903  # <--- Burayı kendi kanal ID'niz ile değiştirin

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Render Port Hatasını Çözmek İçin Web Sunucusu
app = Flask('')

@app.route('/')
def home():
    return "Ses botu aktif ve calisiyor!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    # Bu satır printlerin kesinlikle loglara düşmesini garanti eder
    print(f"{bot.user} olarak Discord'a basariyla giris yapildi!", flush=True)
    
    # Kanalı ID ile çekiyoruz
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    
    if channel is None:
        print(f"HATA: {VOICE_CHANNEL_ID} ID'li kanal bulunamadi! Botun bu kanalin oldugu sunucuda oldugundan ve kanali gorme yetkisi oldugundan emin olun.", flush=True)
        return

    print(f"Kanal bulundu. Adi: {channel.name}, Turu: {type(channel)}", flush=True)
    
    try:
        print("Ses kanalina baglanma istegi gonderiliyor...", flush=True)
        await channel.connect()
        print(f"TEBRIKLER: '{channel.name}' ses kanalina basariyla baglanildi.", flush=True)
    except Exception as e:
        print(f"BAGLANTI HATASI: Ses kanalina baglanirken bir sorun olustu: {e}", flush=True)

if __name__ == "__main__":
    # Web sunucusunu arka planda başlatıyoruz
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.run(TOKEN)