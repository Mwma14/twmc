from pyrogram import Client
import asyncio
from dotenv import load_dotenv

load_dotenv()
import config
from ..logging import LOGGER


assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="MyanmarMusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
            ipv6=False,
        )
        self.two = Client(
            name="MyanmarMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
            ipv6=False,
        )
        self.three = Client(
            name="MyanmarMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
            ipv6=False,
        )
        self.four = Client(
            name="MyanmarMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
            ipv6=False,
        )
        self.five = Client(
            name="MyanmarMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
            ipv6=False,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")

        if config.STRING1:
            await self.one.start()
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Assistant 1 started!")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant 1 failed to send log: {e}")
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant 1 started as {self.one.name}")

        if config.STRING2:
            await self.two.start()
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Assistant 2 started!")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant 2 failed to send log: {e}")
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant 2 started as {self.two.name}")

        if config.STRING3:
            await self.three.start()
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Assistant 3 started!")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant 3 failed to send log: {e}")
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant 3 started as {self.three.name}")

        if config.STRING4:
            await self.four.start()
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "Assistant 4 started!")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant 4 failed to send log: {e}")
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant 4 started as {self.four.name}")

        if config.STRING5:
            await self.five.start()
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "Assistant 5 started!")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant 5 failed to send log: {e}")
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant 5 started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
