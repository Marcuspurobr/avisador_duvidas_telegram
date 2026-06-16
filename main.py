from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio
from tools.notion import checar_duvidas, checar_duvidas_tiradas

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

async def rodar():
    while True:
        await checar_duvidas(bot)
        await checar_duvidas_tiradas(bot)
        await asyncio.sleep(300)

asyncio.run(rodar())