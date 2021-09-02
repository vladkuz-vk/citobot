import logging
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN, counter_file, users_file, result_file
from logic import get_classic_nlm, write_user_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    fullname = message.from_user.full_name
    id = f"user_id: '{str(message.from_user.id)}', username: '{message.from_user.username}', fullname: '{fullname}'\n\n"
    write_user_id(id)
    greet = f"Hi, I'm Cito!\n" \
            f"The easiest way to cite PubMed publications.\n\n" \
            f"To get reference in NLM format, send PMID\n" \
            f"(1 per line, use new line for each one)\n\n" \
            f"Found a bug? Let me know:\n" \
            f"@Vlad_Kuznetsov"
    await message.reply(greet, reply=False)

@dp.message_handler()
async def get_nlm_cite(message: types.Message):
    fullname = message.from_user.full_name
    id = f"user_id: '{str(message.from_user.id)}', username: '{message.from_user.username}', fullname: '{fullname}'\n\n"
    write_user_id(id)
    if all([c.isdigit() or c == '\n' for c in message.text]):
        l = message.text.split()
        if len(l) < 2:
            reference, count = get_classic_nlm(l)
            if count:
                answer = f"{reference}\nI have already made {count} citations!"
                await message.reply(answer, reply=False)
            else:
                await message.reply(reference, reply=False)
        else:
            reference, count = get_classic_nlm(l)
            if count:
                answer = f"I have already made {count} citations!"
                with open(result_file, 'w') as f:
                    f.write(reference)
                await message.answer_document(document=open(result_file, 'rb'))
                await message.reply(answer, reply=False)
            else:
                with open(result_file, 'w') as f:
                    f.write(reference)
                await message.answer_document(document=open(result_file, 'rb'))
    else:
        answer = "Enter PMID only. Use new line for each one.\n" \
                 "Example:\n\n" \
                 "10647931\n" \
                 "21376230\n" \
                 "28890946"
        await message.reply(answer, reply=False)

if __name__ == '__main__':
    executor.start_polling(dp)