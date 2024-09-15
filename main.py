import json, discord, datetime
from discord.ext import commands 

with open('config.json') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with South Bronx'))
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    print(f'{bot.user} has connected to Discord!')



recent_changes = []

gained_today = 0
last_reset = datetime.date.today()

@bot.event
async def on_member_join(member):
    global gained_today
    global last_reset
    if member.guild.id == 1259717095382319215:
        channel = bot.get_channel(1259717946947670098)
        message = await channel.fetch_message(1284732521057226793)
        recent_changes.append('➕')
        if len(recent_changes) > 5:
            recent_changes.pop(0)
        gained_today += 1
        if last_reset != datetime.date.today():
            gained_today = 0
            last_reset = datetime.date.today()
        embed = message.embeds[0]
        embed.description = f'we got {member.guild.member_count} members! | <:upvote:1269483637892714599>\nRecent changes: {"".join(recent_changes)}\nNew Members today: {gained_today}'
        embed.colour = discord.Colour.green()
        await message.edit(embed=embed)

@bot.event
async def on_member_remove(member):
    global gained_today
    global last_reset
    if member.guild.id == 1259717095382319215:
        channel = bot.get_channel(1259717946947670098)
        message = await channel.fetch_message(1284732521057226793)
        recent_changes.append('➖')
        if len(recent_changes) > 5:
            recent_changes.pop(0)
        gained_today -= 1
        if last_reset != datetime.date.today():
            gained_today = 0
            last_reset = datetime.date.today()
        embed = message.embeds[0]
        embed.description = f'we got {member.guild.member_count} members.. | <:downvote:1279377401792434258>\nRecent changes: {"".join(recent_changes)}\nNew Members today: {gained_today}'
        embed.colour = discord.Colour.red()
        await message.edit(embed=embed)
        
@bot.command(name='unban', help='Unbans a user from the server')
@commands.has_any_role(1284509033369305169, 1284508992944476210, 1284508939035349103, 1284508891429736579, 1272930547714232320, 1272963029444595774)
async def unban(ctx, member: discord.User):
    guild_id = 1259717095382319215
    await ctx.send(f'Looking for {member.name}...')
    try:
        (await bot.get_guild(guild_id)).unban(member)
        await ctx.reply(f':white_check_mark:')
    except:
        await ctx.send(f'{member} is not banned! *Maybe you spelled it wrong?*')

bot.run(config['TOKEN'])