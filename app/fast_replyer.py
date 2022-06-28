import asyncio
import json
import sys

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from app.misc.config import (TG_API_HASH, TG_API_ID, TG_CLIENT_NAME,
                             USERS_TO_NOTIFY_TG_IDS, WHEEL_MESSAGE_ID)
from app.misc.consts import (SECOND_CATEGORY, FIFTH_CATEGORY, EIGHTH_CATEGORY, SEVENTH_CATEGORY, FOURTH_CATEGORY,
                             THIRD_CATEGORY, TENTH_CATEGORY, NINETH_CATEGORY,
                             SIXTH_CATEGORY, FIRST_CATEGORY)
from app.setup_logger import logger

categories_list = [NINETH_CATEGORY]

tg_app = Client(TG_CLIENT_NAME, TG_API_ID, TG_API_HASH)

photos_dict = {}


async def send_tg_notification(
        users_ids: list = USERS_TO_NOTIFY_TG_IDS) -> None:
    for id in users_ids:
        await tg_app.send_message(id, 'Message sent.')
        await asyncio.sleep(1)


@tg_app.on_message(filters.reply)
async def my_handler(client: Client, message: Message) -> None:
    if (message.reply_to_message_id == WHEEL_MESSAGE_ID and
            message.from_user is None):
        # text = message.caption.lower()
        await message.reply_photo(
            photo=photos_dict[FIRST_CATEGORY][0],
            reply_to_message_id=message.reply_to_message_id
        )
        await send_tg_notification()
        logger.info('Успех')


async def update_photos():
    try:
        global photos_dict
        for category_name in categories_list:
            current_msg = await tg_app.get_messages(
                "me",
                photos_dict[category_name][1]
            )

            photos_dict[category_name] = (current_msg.photo.file_id,
                                          current_msg.message_id)
        # print(f'photos updated at {datetime.now()}')
    except Exception as e:
        logger.error(f'{str(sys.exc_info())}\n{e}')


async def keep_online() -> None:
    try:
        await tg_app.send(functions.account.UpdateStatus(offline=False))
    except Exception as e:
        logger.error(f'{str(sys.exc_info())}\n{e}')


async def send_photos_to_fav() -> None:
    first = await tg_app.send_photo("me",
                                    photo='misc/pics/1.jpg',
                                    caption=FIRST_CATEGORY)
    photos_dict[FIRST_CATEGORY] = (first.photo.file_id, first.message_id)

    second = await tg_app.send_photo("me",
                                     photo='misc/pics/2.jpg',
                                     caption=SECOND_CATEGORY)
    photos_dict[SECOND_CATEGORY] = (second.photo.file_id, second.message_id)

    third = await tg_app.send_photo("me",
                                    photo='misc/pics/3.jpg',
                                    caption=THIRD_CATEGORY)
    photos_dict[THIRD_CATEGORY] = (third.photo.file_id, third.message_id)

    fourth = await tg_app.send_photo("me",
                                     photo='misc/pics/4.jpg',
                                     caption=FOURTH_CATEGORY)
    photos_dict[FOURTH_CATEGORY] = (fourth.photo.file_id, fourth.message_id)

    fifth = await tg_app.send_photo("me",
                                    photo='misc/pics/5.jpg',
                                    caption=FIFTH_CATEGORY)
    photos_dict[FIFTH_CATEGORY] = (
        fifth.photo.file_id, fifth.message_id
    )

    sixth = await tg_app.send_photo("me",
                                    photo='misc/pics/6.jpg',
                                    caption=SIXTH_CATEGORY)
    photos_dict[SIXTH_CATEGORY] = (
        sixth.photo.file_id, sixth.message_id
    )

    seventh = await tg_app.send_photo("me",
                                      photo='misc/pics/7.jpg',
                                      caption=SEVENTH_CATEGORY)
    photos_dict[SEVENTH_CATEGORY] = (seventh.photo.file_id, seventh.message_id)

    eighth = await tg_app.send_photo("me",
                                     photo='misc/pics/8.jpg',
                                     caption=EIGHTH_CATEGORY)
    photos_dict[EIGHTH_CATEGORY] = (eighth.photo.file_id, eighth.message_id)

    nineth = await tg_app.send_photo("me",
                                     photo='misc/pics/9.jpg',
                                     caption=NINETH_CATEGORY)
    photos_dict[NINETH_CATEGORY] = (
        nineth.photo.file_id, nineth.message_id
    )

    tenth = await tg_app.send_photo("me",
                                    photo='misc/pics/10.jpg',
                                    caption=TENTH_CATEGORY)
    photos_dict[TENTH_CATEGORY] = (
        tenth.photo.file_id, tenth.message_id
    )

    await save_photos_dict()


async def save_photos_dict(client_name: str = TG_CLIENT_NAME) -> None:
    with open(f'misc/photos_dict_{client_name}.json',
              'w',
              encoding="utf8") as f:
        json.dump(photos_dict, f)


def load_photos_dict(client_name: str = TG_CLIENT_NAME) -> None:
    global photos_dict
    try:
        with open(f'misc/photos_dict_{client_name}.json',
                  mode='r',
                  encoding="utf8") as f:
            photos_dict = json.load(f)
    except Exception as e:
        logger.error(e)
