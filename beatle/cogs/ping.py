from discord.ext import commands


class Ping(commands.Cog):
    """Simple ping command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """Respond with 'Pong!'"""
        await ctx.send("Pong!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
