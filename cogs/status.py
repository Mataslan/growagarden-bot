from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="checkstatus")
    async def check_status(self, ctx):
        await ctx.send("✅ Bot status active!")

async def setup(bot):
    await bot.add_cog(Status(bot))
