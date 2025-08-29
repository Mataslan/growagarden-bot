import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import pytz
import config

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_task.start()

    @commands.command(name="verify")
    @commands.has_any_role(config.ROLES["admin"], config.ROLES["moderator"])
    async def verify_user(self, ctx, member: discord.Member):
        """Assign Verified Trader role and log to channel"""
        role = ctx.guild.get_role(config.ROLES["verified_trader"])
        await member.add_roles(role)

        verified_channel = self.bot.get_channel(config.CHANNELS["verified_traders"])
        await verified_channel.send(f"✅ {member.mention} has been verified as a trader!")

        await ctx.send(f"{member.mention} is now verified!")

    @tasks.loop(minutes=1)
    async def daily_task(self):
        """Every day at 16:00 LT send the list of verified users"""
        lt = pytz.timezone("Europe/Vilnius")
        now = datetime.now(lt)

        if now.hour == 16 and now.minute == 0:  # 16:00 LT
            guild = self.bot.get_guild(config.GUILD_ID)
            role = guild.get_role(config.ROLES["verified_trader"])
            members = [m.mention for m in role.members]

            channel = self.bot.get_channel(config.CHANNELS["verified_traders"])
            if members:
                await channel.send("📢 Daily Verified Traders:\n" + "\n".join(members))
            else:
                await channel.send("📢 No verified traders yet.")

    @daily_task.before_loop
    async def before_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Verify(bot))
