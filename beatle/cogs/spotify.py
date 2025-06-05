from __future__ import annotations

import os
from typing import Optional

from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Spotify(commands.Cog):
    """Commands for interacting with Spotify."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sp = self._create_spotify_client()

    def _create_spotify_client(self) -> Optional[spotipy.Spotify]:
        """Create and return a Spotipy client if credentials are available."""
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        if not client_id or not client_secret:
            return None
        auth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        return spotipy.Spotify(auth_manager=auth)

    @commands.command(name="spotify")
    async def search(self, ctx: commands.Context, *, query: str) -> None:
        """Search Spotify for a track and return the first result."""
        if not self.sp:
            await ctx.send("Spotify credentials not configured.")
            return
        results = self.sp.search(q=query, type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            await ctx.send("No tracks found.")
            return
        track = tracks[0]
        name = track.get("name")
        artists = ", ".join(a.get("name") for a in track.get("artists", []))
        url = track.get("external_urls", {}).get("spotify", "")
        await ctx.send(f"{name} by {artists}\n{url}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Spotify(bot))
