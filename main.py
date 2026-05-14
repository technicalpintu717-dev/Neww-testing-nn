import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
API_ID = "27157163"
API_HASH = "e0145db12519b08e1d2f5628e2db18c4"
BOT_TOKEN = "8325851971:AAHQnEfumrJwcz_Ncet34PIBI0XQFP2iFnw"

bot = Client("VOIDxBAN_PRO", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_stats():
    s_count = len([f for f in os.listdir("sessions/") if f.endswith(".session")]) if os.path.exists("sessions/") else 0
    p_count = 0
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r") as f:
            p_count = len([line for line in f if line.strip() and not line.startswith("#")])
    return s_count, p_count

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    s, p = get_stats()
    # UI Design matching 1000679456.jpg
    caption = (
        "**🔱 VOIDxBAN PREMIUM CORE**\n\n"
        f"📱 **Live Sessions:** `{s}/500`\n"
        f"🌐 **Active Proxies:** `{p}`\n"
        "⚡ **Status:** `SYSTEM READY`"
    )
    menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 START ATTACK", callback_data="ask_target")],
        [InlineKeyboardButton("📱 Manage Sessions", callback_data="ms"), 
         InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ])
    await message.reply_text(caption, reply_markup=menu)

@bot.on_callback_query(filters.regex("ask_target"))
async def ask_target(client, query):
    await query.message.edit_text("**🎯 STEP 1:** Target ka Username ya Link bhejo.")

@bot.on_message(filters.text & ~filters.command("start"))
async def get_count(client, message):
    target = message.text
    menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 100 Reports", callback_data=f"atk_100_{target}"),
         InlineKeyboardButton("💥 200 Reports", callback_data=f"atk_200_{target}")]
    ])
    await message.reply_text(f"**Target:** `{target}`\nChoose Intensity:", reply_markup=menu)

@bot.on_callback_query(filters.regex(r"atk_(\d+)_(.+)"))
async def run_attack(client, query):
    count = query.data.split("_")[1]
    target = query.data.split("_")[2]
    _, p = get_stats()
    # Live Attack Screen from 1000679457.jpg
    await query.message.edit_text(
        f"**🔥 ATTACK IN PROGRESS 🔥**\n\n"
        f"🎯 **Target:** `{target}`\n"
        f"✅ **Successful:** `Initiating...`\n"
        f"⏳ **Target Count:** `{count}`\n"
        f"🌐 **Proxies:** `{p}`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛑 STOP", callback_data="refresh")]])
    )

bot.run()
