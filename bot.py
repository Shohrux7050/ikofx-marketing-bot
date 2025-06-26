from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))       # Shohrux ID
HELPER_ID = int(os.getenv("HELPER_ID"))     # Tillo_SnR ID
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))   # Kanal ID (minus bilan)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

referrals = {}

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status != 'left'
    except:
        return False

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"

    if not await check_subscription(user_id):
        await message.answer("🔒 Iltimos, avvalo kanalga obuna bo‘ling: https://t.me/iko_fx")
        return

    if args:
        try:
            referrer_id = int(args)
            if referrer_id != user_id:
                if referrer_id not in referrals:
                    referrals[referrer_id] = set()
                referrals[referrer_id].add(user_id)

                if len(referrals[referrer_id]) == 50:
                    msg = f"🎉 Foydalanuvchi @{username} 50 ta odamni kanalga qo‘shdi!"
                    await bot.send_message(ADMIN_ID, msg)
                    await bot.send_message(HELPER_ID, msg)
        except:
            pass

    await message.answer("✅ Xush kelibsiz! Sizni ko‘rib turganimizdan mamnunmiz!")

@dp.message_handler(commands=['stat'])
async def stat(message: types.Message):
    user_id = message.from_user.id
    count = len(referrals.get(user_id, set()))
    await message.answer(f"📊 Siz {count} ta foydalanuvchini taklif qilgansiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)