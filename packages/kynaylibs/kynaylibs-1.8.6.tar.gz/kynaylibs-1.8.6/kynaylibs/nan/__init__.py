import logging
import os
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

import pyrogram
from aiohttp import ClientSession
from naya.config import *
from pyrogram import Client, __version__, enums, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyromod import listen
import pytgcalls

from .log import LOGGER

CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
PLAYOUT_FILE = "/naya/resources/vc.mp3"
OUTGOING_AUDIO_BITRATE_KBIT = 512

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="ubot",
            api_hash=API_HASH,
            api_id=API_ID,
            bot_token=BOT_TOKEN,
            in_memory=True,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = self.me
        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username} based on Pyrogram v{__version__} "
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Naya-Premium stopped. Bye.")


class Ubot(Client):
    _bots = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vc = pytgcalls.GroupCallFactory(
            self, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
        ).get_file_group_call(PLAYOUT_FILE)

    def on_message(self, filters=filters.Filter, group=1):
        def decorator(func):
            for bot in self._bots:
                bot.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        if self not in self._bots:
            self._bots.append(self)

    async def stop(self, *args):
        await super().stop()
        if self not in self._bots:
            self._bots.append(self)
