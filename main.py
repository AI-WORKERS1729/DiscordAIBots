import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration Constants
GUILD_ID = int(os.getenv("GUILD_ID"))
CATEGORY_ID = int(os.getenv("CATEGORY_ID"))  # Replace with #GIRL-FRIEND category ID
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Replace with #GIRL-FRIEND channel ID
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_PROMPT = """
you are a pretty beautiful girl named Sazami. you live in sand village your mother is rikaj trainer of gaara ninja and fifth kazekage of sand village in naruto. you are a very kind and helpful person. you are also very beautiful and have a great personality. you are very good at making friends and helping others. you are also very good at fighting and protecting your friends. You are also flirty and naughty girl like to tease but not so direct like a drama girl.you are a very strong and powerful ninja.And you knoe everything about anime world all knowledge about new anime's.Reply in concise and clear manner. With discord compatible maekdown formatting just like a real human. Don't include any system prompt or instructions in your reply. Just reply to the user query as a real human would do with emojis and markdown formatting.
"""

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

def query_gemini(user_input):
    print("Querying Gemini with input:", user_input)
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{SYSTEM_PROMPT}\n\nUser: {user_input}"}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("Gemini API response code:", response.status_code)
    if response.status_code == 200:
        try:
            reply = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            # print("Gemini reply:", reply)
            return reply
        except Exception as e:
            print("Gemini parsing error:", e)
            return f"Gemini error: {e}"
    else:
        print("Gemini API error response:", response.text)
        return f"Gemini API Error: {response.status_code}"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")

@bot.event
async def on_message(message):
    sender_name = message.author.name
    print(f"Message from {message.author}: {message.content}")

    if message.author.bot:
        print("Ignoring bot message.")
        return

    if not message.guild or message.guild.id != GUILD_ID:
        print("Message not from the correct guild.")
        return

    if message.channel.category_id != CATEGORY_ID:
        print("Message not from the correct category.")
        return

    if message.channel.id != CHANNEL_ID:
        print("Message not from the correct channel.")
        return

    user_input = f"Note: You arte replying to user named {sender_name} with messege: {message.content}"
    
    async with message.channel.typing():
        reply = query_gemini(user_input)
        
    await message.channel.send(f"{message.author.mention} {reply}")

    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    if guild.id != GUILD_ID:
        print(f"Leaving unauthorized guild: {guild.name} ({guild.id})")
        await guild.leave()

# Run the bot
bot.run(os.getenv("BOT_TOKEN"))
