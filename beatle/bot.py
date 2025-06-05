"""Base classes for building Discord bots."""
from __future__ import annotations

import logging
import pkgutil
import importlib
from typing import Iterable

import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class BeatleBot(commands.Bot):
    """A small extensible bot that auto-loads cogs from a package."""

    def __init__(self, *, command_prefix: str = "!", intents: discord.Intents | None = None,
                 cogs_package: str = "beatle.cogs"):
        intents = intents or discord.Intents.default()
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.cogs_package = cogs_package

    async def setup_hook(self) -> None:
        """Load cogs from the configured package when the bot is starting."""
        try:
            package = importlib.import_module(self.cogs_package)
        except ModuleNotFoundError:
            log.warning("Cogs package %s not found", self.cogs_package)
            return

        if not hasattr(package, "__path__"):
            log.warning("%s is not a package", self.cogs_package)
            return

        for module in pkgutil.iter_modules(package.__path__):
            if module.name.startswith("_"):
                continue
            ext = f"{self.cogs_package}.{module.name}"
            try:
                await self.load_extension(ext)
                log.info("Loaded extension %s", ext)
            except Exception:
                log.exception("Failed to load extension %s", ext)

    def run(self, token: str, *, reconnect: bool = True) -> None:  # pragma: no cover - thin wrapper
        super().run(token, reconnect=reconnect)
