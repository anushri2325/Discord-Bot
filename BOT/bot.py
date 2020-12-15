import discord
import random
import os
from discord.ext import commands,tasks
from itertools import cycle

status = cycle(['Status 1', 'Status 2'])

client =commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    change_status.start()   
    print('Bot is ready!')

@client.event
async def on_member_join(member):
    print(f'{ member } has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{ member } has left a server.')

@client.command()
async def hi(ctx):
    await ctx.send('Welcome to Anushri\'s World')

@client.command(aliases=['8ball'])
async def _8ball(ctx,*,question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
# @has_permissions(administrator=True)
async def kick(ctx, member :discord.Member, *, reason=None ):
    if ctx.message.author.guild_permissions.administrator:
        await member.kick(reason=reason)
    else:
        await ctx.send('oops! you cant')



@client.command()
async def ban(ctx, member :discord.Member, *, reason=None ):
    await member.ban(reason=reason)

@client.command()
async def unban(ctx,*,member):
    #guild.bans returns a tuple 
    banned_users = await ctx.guild.bans()  
    member_name,member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name,user.discriminator) == (member_name , member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
             
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))



# @client.command()
# async def join(ctx):
#     author = ctx.message.author
#     channel = author.voice_channel 
#     await client.join_voice_channel(channel)
@client.command()
async def join( ctx, *, channel: discord.VoiceChannel):
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


client.run('NzQ4ODk3OTczNTgwMjAxOTk1.X0kHlg.cwoFMdh8LPJWFmkP1KaU1S7Tu_U')
