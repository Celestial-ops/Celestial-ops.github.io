import discord
import requests
import os
from flask import Flask
from threading import Thread
from discord.ext import commands

# --- FLASK WEB SERVER (For Railway to stay alive) ---
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head><title>Roblox Linker</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>Roblox Supporter Linker is Online</h1>
            <p>Go to Discord and use <b>!roblox</b> to get started.</p>
            <a href="https://www.roblox.com/game-pass/1759454987/Ac-mods">Buy Gamepass Here</a>
        </body>
    </html>
    """

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# --- DISCORD BOT LOGIC ---
TOKEN = os.environ.get('DISCORD_TOKEN') # We will set this in Railway
GAMEPASS_ID = 1759454987
ROLE_ID = 1485013645615304786
WEBHOOK_URL = "https://discord.com/api/webhooks/1467137149873819710/oDpNM0_05l4BLYpA6yri4jQ_mB14fvJF5wkOOsMozD4KNM17kBXFmb189GWvxr2-r_kb"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

linked_accounts = {}

@bot.command()
async def roblox(ctx):
    await ctx.send(f"🛒 **Buy the gamepass here:** https://www.roblox.com/game-pass/{GAMEPASS_ID}/Ac-mods\nThen type `!link [YourUsername]`")

@bot.command()
async def link(ctx, rbx_username: str):
    try:
        # Get User ID
        user_data = requests.get(f"https://users.roblox.com/v1/users/search?keyword={rbx_username}&limit=1").json()
        if not user_data['data']:
            return await ctx.send("❓ Roblox username not found.")
        
        rbx_id = user_data['data'][0]['id']

        if rbx_id in linked_accounts.values():
            return await ctx.send("⚠️ This Roblox account is already linked.")

        # Check Ownership
        # Using the public API (Requires user inventory to be public)
        check = requests.get(f"https://inventory.roblox.com/v1/users/{rbx_id}/items/1/{GAMEPASS_ID}/is-owned")
        
        if check.text == "true":
            role = ctx.guild.get_role(ROLE_ID)
            if role:
                await ctx.author.add_roles(role)
                linked_accounts[ctx.author.id] = rbx_id
                await ctx.send(f"✅ **Linked!** You now have the {role.name} role.")
                
                # Webhook Log
                requests.post(WEBHOOK_URL, json={"content": f"🔔 {ctx.author} linked to Roblox: `{rbx_username}`"})
            else:
                await ctx.send("❌ Error: Supporter role ID is incorrect.")
        else:
            await ctx.send("❌ You don't own the gamepass yet! Buy it and wait a minute.")
            
    except Exception as e:
        await ctx.send(f"Developer Error: {e}")

# Start both
if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.run(TOKEN)
