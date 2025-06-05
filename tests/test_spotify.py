import asyncio
import discord
from discord.ext import commands
import pytest

from beatle.cogs import spotify as spotify_cog


class DummySpotify:
    def search(self, q, type, limit):
        return {
            "tracks": {
                "items": [
                    {
                        "name": "Song",
                        "artists": [{"name": "Artist"}],
                        "external_urls": {"spotify": "https://example.com"},
                    }
                ]
            }
        }


@pytest.mark.asyncio
async def test_spotify_cog_setup(monkeypatch):
    monkeypatch.setattr(spotify_cog.Spotify, "_create_spotify_client", lambda self: DummySpotify())
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
    await spotify_cog.setup(bot)
    assert "Spotify" in bot.cogs
    cog = bot.cogs["Spotify"]
    messages = []

    async def _send(self, message):
        messages.append(message)

    ctx = type("Ctx", (), {"send": _send})()
    await cog.search.callback(cog, ctx, query="test")
    assert any("Song" in m for m in messages)
