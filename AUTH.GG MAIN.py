
import discord
import requests
import PyAuthGG
from discord.ext import commands
import json
from AuthGG.client import Client
import os
import discord.utils
import time





with open("config.json") as f:
    config = json.load(f)
token = config.get("token")
prefix = config.get("prefix")
api = config.get("api_key")
secret = config.get("secret")
aid = config.get("aid")
auth = config.get("auth key")
pic = config.get("embed_pic")
server_id = int(config.get("server_id"))
verified_role_id = int(config.get("verified_role_id"))

Admin = PyAuthGG.Administration(auth)

App = PyAuthGG.Application(api, aid, secret)

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)
adminclient = PyAuthGG.Administration(auth)
client = PyAuthGG.Application(api, aid, secret)

import colorama
from colorama import Fore, Back, Style

print(f"{Fore.RED}                               .888.      `888'     `8' 8'   888   `8 `888'   `888' ")
print(f"{Fore.RED}                              .8' `888.     888       8       888       888ooooo888  ")
print(f"{Fore.RED}                             .88ooo8888.    888       8       888       888     888  ")
print(f"{Fore.RED}                            .8'     `888.   `88.    .8'       888       888     888  ")
print(f"{Fore.RED}                           o88o     o8888o    `YbodP'        o888o     o888o   o888o ")

print(f"{Fore.RED}                                        oooooooooo.    .oooooo.   ooooooooooooo")
print(f"{Fore.RED}                                        `888'   `Y8b  d8P'  `Y8b  8'   888   `8 ")
print(f"{Fore.RED}                                         888     888 888      888      888      ")
print(f"{Fore.RED}                                        888oooo888' 888      888      888      ")
print(f"{Fore.RED}                                       888    `88b 888      888      888      ")
print(f"{Fore.RED}                                      888    .88P `88b    d88'      888      ")
print(f"{Fore.RED}                                      o888bood8P'   `Y8bood8P'      o888o    ")
print(f"{Fore.RED}=======================================================================================================================")


@bot.event
async def on_ready():
    print(f"                                              {Fore.RED}Thanks for buying!")


@bot.command(brief="Get user info including all used licenses", description="User Info Command",
             help="Get user info including all used licenses")
@commands.has_role("Auth Admin")
async def userinfo(ctx, *, username):
    try:
        result = adminclient.FetchUser(username)
        user_licesnses = adminclient.FetchUsedLicenses(username)
        embed_list = []
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"User Info for {username}")
            embed.add_field(name="__Username__", value=result['username'], inline=False)
            embed.add_field(name="__Email__", value=result['email'], inline=False)
            embed.add_field(name="__HWID__", value=result['hwid'] if result['hwid'] != '' else "Not Set", inline=False)
            embed.add_field(name="__Rank__", value=result['rank'], inline=False)
            embed.add_field(name="__Variable__", value=result['variable'] if result['variable'] != '' else "Not Set",
                            inline=False)
            embed.add_field(name="__Last Login__",
                            value=result['lastlogin'] if result['lastlogin'] != '' else "Not Set", inline=False)
            embed.add_field(name="__Last IP__", value=result['lastip'] if result['lastip'] != '' else "Not Set",
                            inline=False)
            embed.add_field(name="__Expire Date__", value=result['expiry'], inline=False)
            embed_list.append(embed)
            for i in range(len(user_licesnses['Licenses'])):
                licenseinfo = user_licesnses['Licenses'][i]
                licenseembed = discord.Embed(color=0xffbb00, title=f"Used License #{i + 1}")
                licenseembed.add_field(name="__Key__", value=licenseinfo['token'], inline=False)
                licenseembed.add_field(name="__Days__", value=licenseinfo['days'], inline=False)
                licenseembed.add_field(name="__Rank__", value=licenseinfo['rank'], inline=False)
                licenseembed.add_field(name="__Used__", value="True" if licenseinfo['used'] == "1" else "False",
                                       inline=False)
                licenseembed.add_field(name="__Used By__", value=licenseinfo['used_by'], inline=False)
                embed_list.append(licenseembed)
            for _embed in embed_list:
                await ctx.send(embed=_embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: User Not Found")
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        await ctx.send(embed=embed)


@bot.command(aliases=['deluser'], brief="Delete a user", description="Delete User Command", help="Delete a user")
@commands.has_role("Auth Admin")
async def deleteuser(ctx, *, username):
    try:
        result = adminclient.DeleteUser(username)
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"User {username} has been deleted")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: User Not Found")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        embed.set_thumbnail(url=pic)
        await ctx.send(embed=embed)


@bot.command(brief="Get the user count", description="User Count Command", help="Get the user count")
@commands.has_role("Auth Admin")
async def usercount(ctx):
    try:
        result = adminclient.FetchLicenseCount()
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"User Count: {result['value']}")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: Failed to get user count")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        embed.set_thumbnail(url=pic)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_role("Auth Admin")
async def changepass(ctx, name, newpass):
    try:
        result = Admin.ChangePassword(name, newpass)
        print(result)
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"success: {result['info']}")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: Failed to change password")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        embed.set_thumbnail(url=pic)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_role("Auth Admin")
async def changevar(ctx, name, newvar):
    try:
        result = Admin.ChangeVariable(name, newvar)
        print(result)
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"success: {result['info']}")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: Failed to change varible")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        embed.set_thumbnail(url=pic)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_role("Auth Admin")
async def changerank(ctx, name, number):
    try:
        result = Admin.ChangeRank(name, number)
        print(result)
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"success: {result['info']}")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: Failed to change rank")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        embed.set_thumbnail(url=pic)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_role("Auth Admin")
async def resethwid(ctx, *, username):
    try:
        result = Admin.ResetHWID(username)
        print(result)
        if result['status'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"success: {result['info']}")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: Failed to resest HWID Sorry.")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        await ctx.send(embed=embed)


@bot.command()
async def register(ctx, key, name, email, password):
    try:
        result = App.Register(key, name, email, password)
        print(result)
        if result['result'] == "success":
            embed = discord.Embed(color=0x20d420, title=f"account made: {result['result']}")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000, title="Error: Failed to make account.")
            embed.set_thumbnail(url=pic)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xff0000, title=f"Error: {e}")
        await ctx.send(embed=embed)


@bot.command()
@commands.dm_only()
async def verify(ctx, name, number):
    result = App.Login(name, number)
    print(result)
    if result["result"] == "success":
        await ctx.send("Successfully Verified")
        guild = bot.get_guild(server_id)
        role = guild.get_role(verified_role_id)
        member = guild.get_member(ctx.author.id)
        await member.add_roles(role)
    else:
        await ctx.send("Key is not valid")


@verify.error
async def verify_error(ctx, error):
    return


@bot.listen()
async def on_message(message):
    if message.content.startswith(".verify"):
        if isinstance(message.channel, discord.channel.DMChannel):
            return
        else:
            await message.author.send("Please type `.verify <key>` to get verified on the server")


# ---------------help commands
bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Pick a option! ", description="Help section", color=0x00ff40)
    embed.set_thumbnail(url=pic)
    embed.add_field(name="USER", value="All user commands   ", inline=True)
    embed.add_field(name="ADMIN", value="All admin commands", inline=True)
    embed.set_footer(text="AUTH BOT")
    await ctx.send(embed=embed)


@bot.command()
async def user(ctx):
    embed = discord.Embed(title="User commands", color=0x00ff11)
    embed.set_thumbnail(url=pic)
    embed.add_field(name="Register", value="Register (key) (name) (email/discordtag) (password)", inline=True)
    embed.add_field(name="undefined", value="undefined", inline=False)
    embed.set_footer(text="AUTH BOT")
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role("Auth Admin")
async def admin(ctx):
    embed = discord.Embed(title="Admin commands", description="All admin commands listed below", color=0x00ff11)
    embed.set_thumbnail(url=pic)
    embed.add_field(name="Change Password ", value="chnagepass (user) (newpass)", inline=False)
    embed.add_field(name=" Change Rank", value="changerank (name) (number)", inline=False)
    embed.add_field(name="Change varible ", value="chnagevar name (new variable)", inline=False)
    embed.add_field(name="User count", value="usercount", inline=False)
    embed.add_field(name="Delete user ", value="deleteuser (username)", inline=False)
    embed.add_field(name="User info", value="userinfo (username)", inline=False)
    embed.add_field(name="Reset HWID", value="resethwid (username)", inline=True)
    embed.set_footer(text="AUTH BOT")
    await ctx.send(embed=embed)



result = App.Login("test123", "123")
print (result)

bot.run(token)
