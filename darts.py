import asyncio
import logging

from telethon.tl.types import InputMediaDice

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(DartsMod())


@loader.tds
class DartsMod(loader.Module):
    """Darts"""
    strings = {"name": "Дартс🎯",
               "darts_emoji_cfg_doc": "The emoji to be sent to Telegram as a dart's. Can currently be either 🎲 or 🎯"}

    def __init__(self):
        self.config = loader.ModuleConfig("DICE_EMOJI", "'\U0001f3af'", lambda: self.strings["darts_emoji_cfg_doc"])

    def config_complete(self):
        self.name = self.strings["name"]

    async def dartscmd(self, message):
        """Rolls a darts (optionally with the specified value)(edited by @mpamop)"""
        args = utils.get_args(message)
        values = set()
        try:
            for val in args[0].split(","):
                value = int(val)
                if value >= 1 and value <= 6:
                    values.add(value)
        except (ValueError, IndexError):
            values.clear()
        try:
            count = int(args[1])
        except (ValueError, IndexError):
            count = 1
        rolled = -1
        done = 0
        chat = message.to_id
        client = message.client
        while True:
            task = client.send_message(chat, file=InputMediaDice(self.config["DICE_EMOJI"]))
            if message:
                message = (await asyncio.gather(message.delete(), task))[1]
            else:
                message = await task
            rolled = message.media.value
            logger.debug("Rolled %d", rolled)
            if rolled in values or not values:
                done += 1
                message = None
                if done == count:
                    break