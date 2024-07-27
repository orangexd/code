import asyncio
import discord
from discord.ext import commands
import os
import json
import time

# Initialize the bot with intents
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

CHEATS_FILE = "cheats_status.txt"
LAST_MSG_ID_FILE = "last_msg_id.txt"
CHANNEL_ID = 1266674078501048341
GUILD_ID = 806541383363330069
BOT_OWNER_ID = 1264040231213072394

# Load cheats from file
def load_cheats():
    if os.path.exists(CHEATS_FILE):
        with open(CHEATS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save cheats to file
def save_cheats(cheats):
    with open(CHEATS_FILE, "w") as file:
        json.dump(cheats, file)

# Load last message ID from file
def load_last_msg_id():
    if os.path.exists(LAST_MSG_ID_FILE):
        with open(LAST_MSG_ID_FILE, "r") as file:
            return int(file.read().strip())
    return None

# Save last message ID to file
def save_last_msg_id(msg_id):
    with open(LAST_MSG_ID_FILE, "w") as file:
        file.write(str(msg_id))

cheats = load_cheats()

# Create embed from cheats
def create_cheat_embed():
    embed = discord.Embed(
        title="🛠 Exploit Statuses 🛠",
        description=f"This embed will show all the statuses of the major exploits. If you want an exploit to be added here contact {bot.get_guild(GUILD_ID).get_member(BOT_OWNER_ID).mention}.",
    )
    for cheat, data in cheats.items():
        status = data['status']
        if 'timestamp' in data:
            status += f" (since <t:{data['timestamp']}:R>)"
        embed.add_field(name=cheat, value=f"Reported {status}", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/818335750449790986/1266585721087594648/Roblox_exploiting.jpg")
    embed.set_footer(text="Made by Orange, hosted using Infract")
    return embed

# Create second embed
def create_bot_info_embed():
    embed2 = discord.Embed(
        title="🤖 Bot Information 🤖",
        description=f"Created by {bot.get_guild(GUILD_ID).get_member(BOT_OWNER_ID).mention} for r/ROBLOXExploiting. This bot is being hosted on [Infract.WTF](https://infract.wtf). With Love from Orange."
    )
    embed2.add_field(name=f"If you have the role to manage the bot exploit statuses, run !help in {bot.get_guild(GUILD_ID).get_channel(817101108354482198).mention}.", value="Errors are sent directly to Orange.")
    embed2.set_footer(text="Made by Orange, hosted using Infract")
    return embed2

# Bot startup event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    last_msg_id = load_last_msg_id()
    last_msg = None

    if last_msg_id:
        try:
            last_msg = await channel.fetch_message(last_msg_id)
        except discord.NotFound:
            pass

    embed = create_cheat_embed()
    embed2 = create_bot_info_embed()

    if last_msg:
        await last_msg.edit(content="", embeds=[embed, embed2])
    else:
        await channel.purge()
        msg = await channel.send("", embeds=[embed, embed2])
        save_last_msg_id(msg.id)

# Command to add a cheat
@bot.command()
async def addcheat(ctx, status: str, *, name: str):
    if ctx.message.author.name == "lolorangelol":
        status_emoji = {
            "functioning": "✅",
            "issues": "🟡",
            "downtime": "❌"
        }.get(status.lower(), status)

        cheats[name] = {'status': status_emoji}
        save_cheats(cheats)
        embed = create_cheat_embed()
        embed2 = create_bot_info_embed()
        channel = bot.get_channel(CHANNEL_ID)
        last_msg_id = load_last_msg_id()
        last_msg = None

        if last_msg_id:
            try:
                last_msg = await channel.fetch_message(last_msg_id)
            except discord.NotFound:
                pass

        if last_msg:
            await last_msg.edit(content="", embeds=[embed, embed2])
        else:
            await channel.purge()
            msg = await channel.send("", embeds=[embed, embed2])
            save_last_msg_id(msg.id)

            msgreply = await ctx.reply(f"Cheat '{name}' with status '{status_emoji}' added.")
            await asyncio.sleep(3)
            await msgreply.delete()
            await ctx.message.delete()

# Command to change the status of a cheat
@bot.command()
async def changestatus(ctx, status: str, *, name: str):
    if ctx.message.author.name == "lolorangelol":
        status_emoji = {
            "functioning": "✅",
            "issues": "🟡",
            "downtime": "❌"
        }.get(status.lower(), status)

        if name in cheats:
            if status.lower() in ["issues", "downtime"]:
                cheats[name] = {'status': status_emoji, 'timestamp': int(time.time())}
            else:
                cheats[name] = {'status': status_emoji}
            save_cheats(cheats)
            embed = create_cheat_embed()
            embed2 = create_bot_info_embed()
            channel = bot.get_channel(CHANNEL_ID)
            last_msg_id = load_last_msg_id()
            last_msg = None

            if last_msg_id:
                try:
                    last_msg = await channel.fetch_message(last_msg_id)
                except discord.NotFound:
                    pass

            if last_msg:
                await last_msg.edit(content="", embeds=[embed, embed2])
            else:
                await channel.purge()
                msg = await channel.send("", embeds=[embed, embed2])
                save_last_msg_id(msg.id)

            msgreply = await ctx.reply(f"Cheat '{name}' status changed to '{status_emoji}'.")
            await asyncio.sleep(3)
            await msgreply.delete()
            await ctx.message.delete()
        else:
            await ctx.reply(f"Cheat '{name}' not found.")
