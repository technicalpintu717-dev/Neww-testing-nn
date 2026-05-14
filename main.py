import asyncio
import os
from pyrogram import Client, filters, errors, enums
from pyrogram.raw import functions
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
API_ID = "27157163"
API_HASH = "e0145db12519b08e1d2f5628e2db18c4"
BOT_TOKEN = "8325851971:AAHQnEfumrJwcz_Ncet34PIBI0XQFP2iFnw"

bot = Client("VOIDxBAN_PRO", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_data = {}

# Folder Setup
if not os.path.exists("sessions"): os.makedirs("sessions")

# --- REPORTING ENGINE ---
async def start_mass_report(target, report_count):
    sessions = [f for f in os.listdir("sessions/") if f.endswith(".session")]
    success = 0
    failed = 0

    for i in range(int(report_count)):
        for s in sessions:
            if success >= int(report_count): break
            try:
                # Session ko connect karna
                app = Client(s.replace(".session", ""), api_id=API_ID, api_hash=API_HASH, workdir="sessions/")
                await app.start()
                
                # Reporting Logic (Referencing 1000679457.jpg)
                peer = await app.resolve_peer(target)
                await app.invoke(
                    functions.account.ReportPeer(
                        peer=peer,
                        reason=functions.types.InputReportReasonIllegalDrugs(),
                        message="Reporting for illegal drug distribution and harmful content."
                    )
                )
                success += 1
                await app.stop()
                await asyncio.sleep(1) # Anti-ban delay
            except Exception:
                failed += 1
    return success, failed

# --- BOT COMMANDS ---
@bot.on_message(filters.command("start"))
async def start(client, message):
    s_count = len([f for f in os.listdir("sessions/") if f.endswith(".session")])
    text = (
        f"**🔱 VOIDxBAN PREMIUM CORE**\n\n"
        f"📱 **Live Sessions:** `{s_count}`\n"
        f"⚡ **Status:** `READY`\n\n"
        "1. `/add_phone` - Naya account jodne ke liye\n"
        "2. `/report` - Attack start karne ke liye"
    )
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START ATTACK", callback_data="atk")]])
    await message.reply_text(text, reply_markup=btn)

@bot.on_callback_query(filters.regex("atk"))
async def ask_target(client, query):
    await query.message.edit_text("**🎯 Send Target Link/Username:**\nExample: `https://t.me/target` or `@target`")

@bot.on_message(filters.regex(r"(https?://t\.me/|@)\w+"))
async def get_report_count(client, message):
    target = message.text
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 100 Reports", callback_data=f"do_{target}_100"),
         InlineKeyboardButton("💥 200 Reports", callback_data=f"do_{target}_200")]
    ])
    await message.reply_text(f"**Target:** `{target}`\nSelect Intensity:", reply_markup=btn)

@bot.on_callback_query(filters.regex(r"do_(.*)_(\d+)"))
async def execute_attack(client, query):
    target = query.data.split("_")[1]
    count = query.data.split("_")[2]
    
    await query.message.edit_text(f"**🔥 ATTACK STARTED on {target}...**\n\nCheck terminal for live logs.")
    
    ok, bad = await start_mass_report(target, count)
    
    await query.message.edit_text(
        f"**✅ ATTACK COMPLETED**\n\n"
        f"🎯 **Target:** `{target}`\n"
        f"🚀 **Successful Reports:** `{ok}`\n"
        f"❌ **Failed:** `{bad}`"
    )

# --- LOGIN LOGIC (Jo pehle diya tha) ---
@bot.on_message(filters.command("add_phone"))
async def ph(c, m):
    # (Same add_phone logic from previous message)
    pass

bot.run()
