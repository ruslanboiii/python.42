
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import requests
import random

TOKEN = "7586295469:AAEMRMIlBb5Nigvv-V7WqZB3WoHgdjzuI_U"
API_WEATHER = "dd567cb1221b88cbdfec4ecd30167c93"
API_CURRENCY = "023432c3931874ba1359160c"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Asosiy tugmalar
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add("Ob-havo", "Tasodifiy Fakt")
main_keyboard.add("Valyuta kurslari", "Meme")
main_keyboard.add("Aloqa")

# /start komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Assalomu alaykum! Men yordam berishga tayyorman!", reply_markup=main_keyboard)

# /help komandasi
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("Botdan foydalanish uchun tugmalardan birini bosing yoki buyruqlardan foydalaning.")

# /about komandasi
@dp.message_handler(commands=['about'])
async def about_command(message: types.Message):
    await message.answer("Bu bot sizga ob-havo, valyuta kurslari va qiziqarli faktlar haqida ma'lumot beradi.")

# /settings komandasi
@dp.message_handler(commands=['settings'])
async def settings_command(message: types.Message):
    await message.answer("Sozlamalar bo'limi hozirda ishlanmoqda.")

# Ob-havo
@dp.message_handler(lambda message: message.text == "Ob-havo")
async def ask_city(message: types.Message):
    await message.answer("Shahar nomini kiriting:")

@dp.message_handler(lambda message: message.text and len(message.text) > 2 and message.text not in ["Ob-havo", "Tasodifiy Fakt", "Valyuta kurslari", "Meme", "Aloqa"])
async def get_weather(message: types.Message):
    city = message.text.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric"
    response = requests.get(url).json()

    if "main" in response:
        temp = response["main"]["temp"]
        await message.answer(f"{city} ob-havosi: {temp}°C")
    else:
        await message.answer("Shahar topilmadi! Iltimos, to'g'ri nom kiriting.")

# Tasodifiy fakt
facts = [
    "Dunyo bo'ylab har kuni 8.6 million chaqaloq tug'iladi.",
    "Odam tanasidagi suyaklar soni 206 ta.",
    "Everest tog'ining balandligi 8,848 metr."
]

@dp.message_handler(lambda message: message.text == "Tasodifiy Fakt")
async def random_fact(message: types.Message):
    await message.answer(random.choice(facts))

# Valyuta kurslari
@dp.message_handler(lambda message: message.text == "Valyuta kurslari")
async def get_currency(message: types.Message):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url).json()

    if "rates" in response:
        rates = response["rates"]
        uzs = rates.get("UZS", "Mavjud emas")
        eur = rates.get("EUR", "Mavjud emas")
        rub = rates.get("RUB", "Mavjud emas")
        await message.answer(f"💵 USD: {uzs} UZS\n💶 EUR: {eur} UZS\n🇷🇺 RUB: {rub} UZS")
    else:
        await message.answer("Valyuta ma'lumotlari olinmadi!")

# Meme
@dp.message_handler(lambda message: message.text == "Meme")
async def send_meme(message: types.Message):
    meme_url = "https://i.redd.it/l0x2z8s0p9m61.jpg"
    await message.answer_photo(meme_url)

# Aloqa
@dp.message_handler(lambda message: message.text == "Aloqa")
async def contact_info(message: types.Message):
    await message.answer("Bog'lanish uchun: @rus1anboi")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


