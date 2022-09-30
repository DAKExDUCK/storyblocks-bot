from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot.functions.rights import (is_Admin, secret_words,
                                  users)
from bot.keyboards.default import add_delete_button
from bot.objects.logger import logger, print_msg


@is_Admin
async def send_log(message: types.Message):
    with open('logs.log', 'r') as logs:
        await message.reply_document(logs)


@print_msg
async def enter_secret(message: types.Message, state: FSMContext):
    if message.text in secret_words:
        users.append(message.from_user.id)
        await message.reply('Вы получили доступ к боту\n' \
            'Отправьте ссылку для скачки видео с сайта storyblocks',
            reply_markup=add_delete_button())
    else:
        await message.reply('Неправильное кодовое слово. Попробуй еще раз',
            reply_markup=add_delete_button())


async def all_errors(update: types.Update, error):
    # update_json = {}
    # update_json = json.loads(update.as_json())
    # if 'callback_query' in update_json.keys():
    #     await update.callback_query.answer('Error, if you have some troubles, /msg_to_admin')
    #     chat_id = update.callback_query.from_user.id
    #     text = update.callback_query.data
    # elif 'message' in update_json.keys():
    #     await update.message.answer('Error, if you have some troubles, /msg_to_admin')
    #     chat_id = update.message.from_user.id
    #     text = update.message.text
    logger.error(exc_info=True)
    

def register_handlers_secondary(dp: Dispatcher):
    dp.register_message_handler(send_log, commands="get_logfile", state="*")
    dp.register_message_handler(enter_secret, content_types=['text'], state="*")

    dp.register_errors_handler(all_errors)
