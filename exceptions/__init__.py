# https://github.com/TopStop5/Python-Discord-Bot-Template

from discord.ext import commands

"""
DO NOT TOUCH ANYTHING BELOW UNLESS YOU KNOW WHAT YOUR DOING
"""

class UserBlacklisted(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but is blacklisted.
    """

    def __init__(ctx, message="User is blacklisted!"):
        ctx.message = message
        super().__init__(ctx.message)


class UserNotOwner(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but is not an owner of the bot.
    """

    def __init__(ctx, message="User is not an owner of the bot!"):
        ctx.message = message
        super().__init__(ctx.message)