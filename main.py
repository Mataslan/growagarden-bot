import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
initial_extensions = ["cogs.status", "cogs.verify"]

for ext in initial_extensions:
    bot.load_extension(ext)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    guild = bot.get_guild(config.GUILD_ID)
    print(f"Connected to guild: {guild.name} ({guild.id})")

# Keep Alive (Replit uptime robot pings)
keep_alive()

# Run bot with token from secrets
bot.run(os.getenv("DISCORD_TOKEN"))
