from __future__ import annotations

import yt_dlp
import discord
from discord.ext import commands


class YTDLPlayer(commands.Cog):
    """Play audio from URLs using yt-dlp."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ytdl = yt_dlp.YoutubeDL({"format": "bestaudio/best", "quiet": True})

    async def _ensure_voice(self, ctx: commands.Context) -> discord.VoiceClient | None:
        if not getattr(ctx.author, "voice", None):
            await ctx.send("You are not in a voice channel.")
            return None
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            return await channel.connect()
        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)
        return ctx.voice_client

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        """Play audio from a given URL."""
        voice = await self._ensure_voice(ctx)
        if voice is None:
            return
        info = self.ytdl.extract_info(url, download=False)
        source = discord.FFmpegPCMAudio(info["url"])
        voice.play(source)
        title = info.get("title", url)
        await ctx.send(f"Now playing: {title}")

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context) -> None:
        """Stop playback and leave the channel."""
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YTDLPlayer(bot))
