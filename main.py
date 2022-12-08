from telethon import events
from telethon.types import Message
from models import session_db, Content
from configs import (LIST_CHANNELS,
                     client)
import os


class Scraper:
    @staticmethod
    def scraper_new_message(message, file_path):
        date = message[0].date
        msg = message[0].message
        message_id = message[0].id
        channel_id = message[0].peer_id.channel_id

        session_db.add(Content(message_id=message_id,
                               channel_id=channel_id,
                               created_at=date,
                               content=msg,
                               media_content=file_path))

        session_db.commit()

    @staticmethod
    async def download_file(message: Message):
        file_path = await client.download_media(message.media, f"{os.getcwd()}/media/")
        return file_path

    @staticmethod
    def scraper_edited_message(message):
        message_id = message[0].id
        msg = message[0].message
        edited_date = message[0].edit_date
        session_db.query(Content).filter(Content.message_id == message_id).update(
            {"content": msg,
             "edited_at": edited_date,
             "is_edited": True})

        session_db.commit()

    @staticmethod
    def scraper_deleted_message(event):
        for message_id in event.deleted_ids:
            session_db.query(Content).filter(Content.message_id == message_id).update(
                {"is_deleted": True})

            session_db.commit()

    @staticmethod
    @client.on(events.NewMessage(chats=LIST_CHANNELS))
    async def new_message_handler(event):
        chat = await event.get_input_chat()
        msg = await client.get_messages(chat.channel_id)
        file_path = await Scraper.download_file(message=msg[0])
        Scraper.scraper_new_message(message=msg, file_path=file_path)

    @staticmethod
    @client.on(events.MessageEdited(chats=LIST_CHANNELS))
    async def edited_message_handler(event):
        chat = await event.get_input_chat()
        msg = await client.get_messages(chat.channel_id)
        Scraper.scraper_edited_message(message=msg)

    @staticmethod
    @client.on(events.MessageDeleted(chats=LIST_CHANNELS))
    async def deleted_message_handler(event):
        Scraper.scraper_deleted_message(event)

    @classmethod
    def run(cls):
        client.start()
        client.run_until_disconnected()


Scraper.run()
