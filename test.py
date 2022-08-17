# https://Website.com/TopStop5/Python-Discord-Bot-Template


import discord, os, json, checks, exceptions
from discord import Member
from discord.ext import commands
from discord.errors import Forbidden

with open('config.json', 'r') as f:
    config = json.load(f)

with open("blacklist.json") as file:
    blacklistB = json.load(file)


Owners = config.get('owners')
BlacklistedUsers = blacklistB.get('ids')
TOKEN = config.get('TOKEN')
Prefix = config.get('PREFIX')
Invite = config.get('Invite')
Website = config.get('Website')

intents = discord.Intents.all()

client = commands.Bot(command_prefix=Prefix, intents=intents, help_command=None)

@client.event
async def on_ready():
    print('Bot Online')
#   await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} Servers "))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{Prefix}help • {Website}"))

"""
DO NOT TOUCH ANYTHING BELOW UNLESS YOU KNOW WHAT YOUR DOING
"""


def add_user_to_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r+") as file:
        file_data = json.load(file)
        file_data["ids"].append(user_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)

def remove_user_from_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(user_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)

def blacklist_error_add(ctx, user_id: int) -> None:
    print(f"User {user_id} failled being added to the blacklist")
    ctx.send(f"User {user_id} failed being added to the blacklist")
def blacklist_error_remove(ctx, user_id: int) -> None:
    print(f"User {user_id} failled being removed from the blacklist")
    ctx.send(f"**{user_id} failed being removed from the blacklist")
def blacklist_error_add(ctx, user_id: int) -> None:
    print(f"User {user_id} failled being added to the blacklist")

"""
HELP COMMANDS
"""

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**ERROR**! You are still on cooldown! please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, exceptions.UserNotOwner):
        msg = f'**ERROR**! You are Not an Owner of the bot! Think this might be an error? {Prefix}help addowner'
        await ctx.send(msg)

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, exceptions.UserBlacklisted):
        msg = f'**ERROR**! You are **BLACKLISTED** from using this bot!'
        await ctx.send(msg)


@client.group(invoke_without_command=True, aliases=['Help', 'HELP'])
@checks.not_blacklisted()
async def help(ctx):
    embed=discord.Embed(
        title="Help Commands",
        color=0x00ff04
    )
    embed.add_field(
        name="Moderation",
        value=f"{Prefix}help Moderation",
        inline=True
    )
    embed.add_field(
        name="Fun",
        value=f"{Prefix}help Fun",
        inline=True
    )
    embed.add_field(
        name="Other",
        value=f"{Prefix}help Other",
        inline=True
    )
    embed.add_field(
        name="Owner",
        value=f"{Prefix}help Owner",
        inline=True
    )
    embed.set_footer(
        text=f'Check out my Website! {Website}'
    )
    await ctx.reply(embed=embed, mention_author=True)

@help.command()
@checks.not_blacklisted()
async def addowner(ctx):
    embed=discord.Embed(
        title="Command Help: Add Owner",
        description="Make a user Owner of the bot!",
        color=0x8c00ff
    )
    embed.add_field(
        name="Steps",
        value="Open cofig.json and put your user id there"
    )
    await ctx.reply(embed=embed, mention_author=False)

@help.command(aliases=['OWNER', 'Owner'])
@checks.is_owner()
async def owner(ctx):
    embed=discord.Embed(
        title="Help Category: Owner",
        description="Only the bot owner can veiw and use these commands",
        color=0xff7b00
    )
    embed.add_field(
        name="Blacklist",
        value="Blacklist a user and make them un-able to use the bot",
        inline=True
    )
    embed.set_footer(
    text=f'Check out my Website! {Website}'
    )
    await ctx.reply(embed=embed, mention_author=True)

@help.command(aliases=['Moderation', 'MODERATION'])
@checks.not_blacklisted()
@commands.cooldown(1,15,commands.BucketType.user)
async def moderation(ctx):
    embed=discord.Embed(
        title="Help Category: Moderation",
        description=f"For a more in-depth explanation simply type {Prefix}help <command>",
        color=0xff7300
    )
    embed.add_field(
        name="`Kick`",
        value="Kicks the user specified from the server",
        inline=True
    )
    embed.add_field(
        name="`Nick`",
        value="Changes your or the user you @'s nickname to the nickname u requested",
        inline=True
    )
    embed.add_field(
        name="`Ban`",
        value="Bans The user you specifed from the server for the reason you specified",
        inline=True
    )
    embed.add_field(
        name="`HackBan`",
        value="Bans The user you specified from the server (even if they are not in the server)",
        inline=True
    )
    embed.add_field(
        name="`Warn`",
        value="Warns the user you specified for the reason you specified",
        inline=True
    )
    embed.add_field(
        name="`Purge`",
        value="Deletes the amount of messages you requested",
        inline=True
    )
    embed.set_footer(
    text=f'Check out my Website! {Website}'
    )
    await ctx.reply(embed=embed, mention_author=True)

"""
BOT INVITE
"""
@client.command()
@checks.not_blacklisted()
async def invite(ctx):
    if ctx.author.name in BlacklistedUsers:
        return
    embed=discord.Embed(title="Invite", url=Invite, description="Add The client to your server!", color=0xff0000)
    await ctx.send(embed=embed)
"""
BLACKLIST
"""
@client.group(invoke_without_command=True)
@checks.is_owner()
async def blacklist(ctx):
    text=f"There are {len(blacklistB['ids'])} users in the blacklist"
    await ctx.send(text)

@blacklist.command()
@checks.is_owner()
async def add(ctx, member: discord.Member = None):
    with open("blacklist.json") as file:
        blacklistA = json.load(file)
    user_id = member.id
    if user_id in BlacklistedUsers:
        await ctx.send("User Already Blacklisted")
        return
    if checks.is_owner:
        await ctx.send("**HEY**! Thats my owner! You cant do that!")
        return
    try: 
        add_user_to_blacklist(user_id)
        embed=discord.Embed(title="User __Blacklisted__", description=f"**{member.name}** has been successfully added to the blacklist", color=0xff0000)
        embed.set_footer(
        text=f"There are now {len(blacklistA['ids'])} users in the blacklist"
    )
        await ctx.send(embed=embed)
    except:
        blacklist_error_add

@blacklist.command()
@checks.is_owner()
async def remove(ctx, member: discord.Member = None):
    user_id = member.id
    try:
        remove_user_from_blacklist(user_id)
        embed=discord.Embed(title="User Removed From Blacklist", description=f"**{member.name}** has been successfully been removed from the blacklist", color=0x00ff11)
        embed.set_footer(
        text=f'Check out my Website! {Website}'
        )
        await ctx.send(embed=embed)
    except:
        await ctx.send("**HEY**! Thats my owner! You cant do that!")

"""
Kick Command
"""
@client.command()
@commands.has_permissions(kick_members=True)
@checks.not_blacklisted()
async def kick(ctx, member: discord.Member, *, reason: str = "Not specified") -> None:
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
        else:
            try:
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{ctx.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                embed.set_footer(
                text=f'Check out my Website! {Website}'
                )
                await ctx.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{ctx.author}**!\nReason: {reason}"
                    )
                except discord.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                embed.set_footer(
                text=f'Check out my Website! {Website}'
                )
                await ctx.send(embed=embed)
"""
Nick Command
"""
@client.command()
@commands.has_permissions(manage_nicknames=True)
@checks.not_blacklisted()
async def nick(ctx, member: discord.Member, *, nickname: str = None) -> None:
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x00ff40
            )
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            embed.set_footer(
            text=f'Check out my Website! {Website}'
            )
            await ctx.send(embed=embed)
"""
Ban Command
"""
@client.command()
@commands.has_permissions(ban_members=True)
@checks.not_blacklisted()
async def ban(ctx, member: discord.Member, *, reason: str = "Not specified") -> None:
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                embed.set_footer(
                text=f'Check out my Website! {Website}'
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{ctx.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                embed.set_footer(
                text=f'Check out my Website! {Website}'
                )
                await ctx.send(embed=embed)
                try:
                    await member.send(f"You were banned by **{ctx.author}**!\nReason: {reason}")
                except discord.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
"""
Warn Command
"""
@client.command()
@commands.has_permissions(manage_messages=True)
@checks.not_blacklisted()
async def warn(ctx, member: discord.Member, *, reason: str = "Not specified") -> None:
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{ctx.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await ctx.send(embed=embed)
        try:
            await member.send(f"You were warned by **{ctx.author}**!\nReason: {reason}")
        except discord.Forbidden:
            # Couldn't send a message in the private messages of the user
            await ctx.send(f"{member.mention}, you were warned by **{ctx.author}**!\nReason: {reason}")
"""
Purge Command
"""
@client.command()
@commands.has_guild_permissions(manage_messages=True)
@checks.not_blacklisted()
async def purge(ctx, amount: int) -> None:
        try:
            amount = int(amount)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        purged_messages = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Chat Cleared!",
            description=f"**{ctx.author}** cleared **{len(purged_messages)}** messages!",
            color=0x9C84EF
        )
        embed.set_footer(
        text=f'Check out my Github! https://github.com/TopStop5/Python-Discord-Bot-Template'
        )
        await ctx.send(embed=embed)
"""
HackBAN Command
"""
@client.command(aliases=['hban'])
@checks.not_blacklisted()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def hackban(ctx, user_id: int, *, reason: str):
    if user in ctx.guild.members:
            user = await ctx.client.get_or_fetch_user(user_id)
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B
            )
            await ctx.reply(embed=embed, mention_author=False)

    else:
        await ctx.guild.ban(user)
        await ctx.guild.ban(user_id)
        user = await ctx.client.get_or_fetch_user(user_id)
        embed = discord.Embed(
            title="User Banned!",
            description=f"**{user} (ID: {user.id}) ** was banned by **{ctx.author}**!",
            color=0x9C84EF
            )
        embed.add_field(
            name="Reason:",
            value=reason
            )
        await ctx.reply(embed=embed, mention_author=False)

client.run(TOKEN)