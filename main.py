import discord
import requests
import os
import json
from flask import Flask
from threading import Thread
from discord.ext import commands

# --- 1. WEB SERVER TO KEEP RENDER HAPPY ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Online and Running!"

def run_web():
    # Render uses a dynamic port; this line grabs it automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. DATABASE LOGIC (Saves to a file) ---
DATA_FILE = "linked_users.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- 3. BOT CONFIGURATION ---
# IMPORTANT: Set 'DISCORD_TOKEN' in Render's Environment Variables tab
TOKEN = os.environ.get('DISCORD_TOKEN') 
GAMEPASS_ID = 1759454987
ROLE_ID = 1485013645615304786
WEBHOOK_URL = "https://discord.com/api/webhooks/1467137149873819710/oDpNM0_05l4BLYpA6yri4jQ_mB14fvJF5wkOOsMozD4KNM17kBXFmb189GWvxr2-r_kb"

intents = discord.Intents.all() # Gives bot permission to see members and messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')

@bot.command()
async def roblox(ctx):
    await ctx.send(f"🛒 **Buy the gamepass here:** https://www.roblox.com/game-pass/{GAMEPASS_ID}/Ac-mods\nThen type `!link [YourUsername]`")

@bot.command()
async def link(ctx, rbx_username: str):
    linked_accounts = load_data()
    
    try:
        # Get Roblox User ID
        user_res = requests.get(f"https://users.roblox.com/v1/users/search?keyword={rbx_username}&limit=1").json()
        if not user_res.get('data'):
            return await ctx.send("❓ Roblox username not found.")
        
        rbx_id = str(user_res['data'][0]['id'])

        # Check if Roblox ID is already linked to ANYONE
        if rbx_id in linked_accounts.values():
            # Find who it's linked to
            current_owner = "someone"
            for discord_id, rid in linked_accounts.items():
                if rid == rbx_id:
                    current_owner = f"<@{discord_id}>"
                    break
            return await ctx.send(f"⚠️ This Roblox account is already linked to {current_owner}.")

        # Check Gamepass Ownership
        check = requests.get(f"https://inventory.roblox.com/v1/users/{rbx_id}/items/1/{GAMEPASS_ID}/is-owned")
        
        if check.text == "true":
            role = ctx.guild.get_role(ROLE_ID)
            if role:
                await ctx.author.add_roles(role)
                
                # Save to database
                linked_accounts[str(ctx.author.id)] = rbx_id
                save_data(linked_accounts)
                
                await ctx.send(f"✅ **Linked!** You now have the {role.name} role.")
                
                # Webhook Log
                log_data = {"content": f"🎉 **New Link**: {ctx.author.name} linked to `{rbx_username}`"}
                requests.post(WEBHOOK_URL, json=log_data)
            else:
                await ctx.send("❌ Error: I can't find the Supporter role in this server.")
        else:
            await ctx.send("❌ You don't own the gamepass yet! (Ensure your Roblox inventory is **Public**).")
            
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(f"⚠️ An error occurred: {e}")

# --- 4. START EVERYTHING ---
if __name__ == "__main__":
    # Starts the web server so Render doesn't shut us down
    Thread(target=run_web).start()
    # Starts the Discord Bot
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ ERROR: No DISCORD_TOKEN found in Environment Variables!")
