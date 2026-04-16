import discord
from discord.ext import commands
import sqlite3
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# DATABASE
# ======================

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    coins INTEGER DEFAULT 0
)
""")
conn.commit()

# ======================
# HELPERS
# ======================

def create_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def get_user(user_id):
    create_user(user_id)
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

def add_xp(user_id, xp):
    create_user(user_id)
    user = get_user(user_id)

    current_xp = user[1]
    level = user[2]

    current_xp += xp

    while current_xp >= level * 100:
        current_xp -= level * 100
        level += 1

    cursor.execute(
        "UPDATE users SET xp=?, level=? WHERE user_id=?",
        (current_xp, level, user_id)
    )
    conn.commit()

def add_coins(user_id, amount):
    create_user(user_id)
    cursor.execute(
        "UPDATE users SET coins = coins + ? WHERE user_id=?",
        (amount, user_id)
    )
    conn.commit()

# ======================
# EVENTS
# ======================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if len(message.content) < 3:
        return

    add_xp(message.author.id, random.randint(5, 15))
    add_coins(message.author.id, random.randint(1, 5))

    await bot.process_commands(message)

# ======================
# COMMANDS
# ======================

@bot.command()
async def balance(ctx):
    user = get_user(ctx.author.id)
    await ctx.send(f"💰 Coins: {user[3]}")

@bot.command()
async def level(ctx):
    user = get_user(ctx.author.id)
    await ctx.send(f"📈 Level: {user[2]} | XP: {user[1]}")

@bot.command()
async def daily(ctx):
    amount = random.randint(50, 150)
    add_coins(ctx.author.id, amount)
    await ctx.send(f" You received {amount} coins!")

@bot.command()
async def gamble(ctx, amount: int):
    if amount <= 0:
        await ctx.send("❌ Invalid amount!")
        return

    user = get_user(ctx.author.id)

    if user[3] < amount:
        await ctx.send("❌ Not enough coins!")
        return

    if random.random() < 0.5:
        add_coins(ctx.author.id, amount)
        await ctx.send(f"🎉 You won {amount} coins!")
    else:
        cursor.execute(
            "UPDATE users SET coins = coins - ? WHERE user_id=?",
            (amount, ctx.author.id)
        )
        conn.commit()
        await ctx.send(f"💀 You lost {amount} coins!")

bot.run(os.getenv("DISCORD_TOKEN"))