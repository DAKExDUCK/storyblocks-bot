from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.functions.rights import is_user
from bot.objects.logger import logger, print_msg
from bot.keyboards.default import add_delete_button
from bot.functions.tools import parse_cookie_json, get_info


@print_msg
async def start(message: types.Message, state: FSMContext):
    text = "Приветствую! Если ты ученик школы VideoPro, отправь кодовое слово"
    await message.reply(text, reply_markup=add_delete_button())
    await state.finish()


@print_msg
async def video_pars(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    msg_text = message.text
    bot = message.bot
    if is_user(user_id):
        try:
            session = parse_cookie_json('cookies.json')

            url = msg_text
            info = await get_info(url, session)
            thumb = info['details']['stockItem']['thumbnailUrl']
            title = info['details']['stockItem']['title']

            await message.reply_photo(thumb, f'{title}\n\nНачинаю скачивание видео...')

            formats = {}

            for format in info['details']['stockItemFormats']:
                # print(format)
                formats[format['label']] = format

            if '4KMP4' not in formats and 'HDMP4' not in formats:
                form_label = list(formats.keys())[-1]
                download_info_path = formats[form_label]['downloadAjaxUrl']
                async with session.get(f'https://www.storyblocks.com{download_info_path}') as resp:
                    video_url = (await resp.json())['data']['downloadUrl']

                m_text = f'<b>Скачать видео:<b>\n1) Нажмите ПКМ\n2) Нажмите "Сохранить видео"\n\nИли перейдите по ссылке:\n1) <a href="{video_url}">{form_label[:2]} качество</a>\n\n<i>Данное видео недоступно в формате MP4</i>'
            else:
                download_info_path = formats['HDMP4']['downloadAjaxUrl']
                async with session.get(f'https://www.storyblocks.com{download_info_path}') as resp:
                    video_url = (await resp.json())['data']['downloadUrl']

                if '4KMP4' in formats:
                    async with session.get(f'https://www.storyblocks.com{formats["4KMP4"]["downloadAjaxUrl"]}') as resp:
                        _4k_url = (await resp.json())['data']['downloadUrl']
                else:
                    _4k_url = None

                m_text = f'<b>Скачать видео:<b>\n1) Нажмите ПКМ\n2) Нажмите "Сохранить видео"\n\nИли перейдите по ссылке:\n1) <a href="{video_url}">HD качество</a>\n'

                if _4k_url:
                    m_text += f'2) <a href="{_4k_url}">4K качество</a>'
            await session.close()
            try:
                await bot.send_file(user_id, video_url, caption=m_text)
            except Exception as e:
                text_1 = '\n'.join(m_text.split('\n')[5:]) + '\n\n<i>Данное видео весит более 20 МБ, перейдите по ссылке чтобы скачать</i>'
                await bot.send_message(user_id, text_1)
        except KeyError as e:
            logger.error(e)
            await message.reply(f'Необходимо возобновить подписку')
    else:
        await message.reply('Для начала введи кодовое слово!', reply_markup=add_delete_button())



async def delete_msg(query: types.CallbackQuery):
    try:
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        if query.message.reply_to_message:
            await query.bot.delete_message(query.message.chat.id, query.message.reply_to_message.message_id)
        await query.answer()
    except Exception as exc:
        logger.error(exc)
        await query.answer("Error")


def register_handlers_default(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    
    dp.register_message_handler(video_pars, lambda msg: 'storyblocks' in msg.text, content_types=['text'], state="*")


    dp.register_callback_query_handler(
        delete_msg,
        lambda c: c.data == "delete",
        state="*"
    )
