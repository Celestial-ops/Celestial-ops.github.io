import discord
import requests
import os
from flask import Flask
from threading import Thread
from discord.ext import commands

# --- PREVENT RENDER SLEEP ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    # Render provides a PORT environment variable automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
# IMPORTANT: Use Environment Variables in Render Dashboard
TOKEN = os.environ.get('DISCORD_TOKEN') 
GAMEPASS_ID = 1759454987
ROLE_ID = 1485013645615304786
WEBHOOK_URL = "https://discord.com/api/webhooks/1467137149873819710/oDpNM0_05l4BLYpA6yri4jQ_mB14fvJF5wkOOsMozD4KNM17kBXFmb189GWvxr2-r_kb"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Needed to give roles
bot = commands.Bot(command_prefix="!", intents=intents)

linked_accounts = {}

@bot.command()
async def roblox(ctx):
    await ctx.send(f"🔗 **Buy the gamepass here:** https://www.roblox.com/game-pass/{GAMEPASS_ID}/Ac-mods\nThen type `!link [YourUsername]`")

@bot.command()
async def link(ctx, rbx_username: str):
    try:
        # Search for User
        user_res = requests.get(f"https://users.roblox.com/v1/users/search?keyword={rbx_username}&limit=1").json()
        if not user_res.get('data'):
            return await ctx.send("❌ Username not found on Roblox.")
        
        rbx_id = user_res['data'][0]['id']

        # Check if already linked
        if rbx_id in linked_accounts.values():
            return await ctx.send("⚠️ This Roblox account is already linked to a Discord user.")

        # Check Gamepass Ownership
        # Note: Users MUST have their inventory set to "Public" in Roblox settings
        check = requests.get(f"https://inventory.roblox.com/v1/users/{rbx_id}/items/1/{GAMEPASS_ID}/is-owned")
        
        if check.text == "true":
            role = ctx.guild.get_role(ROLE_ID)
            if role:
                await ctx.author.add_roles(role)
                linked_accounts[ctx.author.id] = rbx_id
                await ctx.send(f"✅ **Success!** Linked to `{rbx_username}`. You now have the Supporter role.")
                
                # Webhook Notification
                requests.post(WEBHOOK_URL, json={"content": f"📝 **Link Event**: {ctx.author} linked to `{rbx_username}`"})
            else:
                await ctx.send("❌ Error: I couldn't find the Role ID. Check bot permissions.")
        else:
            await ctx.send("❌ You don't own the gamepass yet. (Make sure your Roblox inventory is **Public**!)")
            
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("⚠️ An error occurred while checking. Try again later.")

if __name__ == "__main__":
    # Start the web server in a separate thread
    Thread(target=run_web).start()
    # Start the bot
    bot.run(TOKEN)
