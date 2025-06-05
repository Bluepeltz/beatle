import discord
from discord.ext import commands
import pytest

from beatle.cogs import ytdl as ytdl_cog


class DummyYTDL:
    def extract_info(self, url, download=False):
        return {"url": "http://audio", "title": "Test"}


class DummyVoiceClient:
    def __init__(self):
        self.played = None
        self.channel = None

    async def move_to(self, channel):
        self.channel = channel

    def play(self, source):
        self.played = source

    async def disconnect(self):
        self.disconnected = True

    def stop(self):
        self.stopped = True


class DummyVoiceChannel:
    async def connect(self):
        return DummyVoiceClient()


class DummyAuthor:
    def __init__(self):
        self.voice = type("Voice", (), {"channel": DummyVoiceChannel()})


class DummyCtx:
    def __init__(self):
        self.author = DummyAuthor()
        self.voice_client = None
        self.sent = []

    async def send(self, msg):
        self.sent.append(msg)


@pytest.mark.asyncio
async def test_play(monkeypatch):
    monkeypatch.setattr(ytdl_cog.yt_dlp, "YoutubeDL", lambda *a, **k: DummyYTDL())
    monkeypatch.setattr(discord, "FFmpegPCMAudio", lambda url: url)

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
    await ytdl_cog.setup(bot)
    cog = bot.cogs["YTDLPlayer"]
    ctx = DummyCtx()
    await cog.play.callback(cog, ctx, url="http://example.com")
    assert any("Now playing" in m for m in ctx.sent)
