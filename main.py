import json, discord, datetime, random, asyncio
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

words = [
    'nigger',
    'faggot',
    'rape'
]

@bot.event
async def on_message(message):
    if any(word in message.content.lower() for word in words):

        user = bot.get_user(814226043924643880)
        user2 = bot.get_user(1021228427442933831)
        channel = await user.create_dm()
        channel2 = await user2.create_dm()
        embed = discord.Embed(title='**SOMEONE SAID A BAD WORD**', description=f'**{message.author.mention}**\n`{message.content}`', color=discord.Colour.red())
        embed.set_footer(text="That guy should get in trouble ngl")
        embed.set_author(name=message.author.name)
        await channel.send(embed=embed)
        await channel2.send(embed=embed)
        """while True:
            await message.channel.send("hi can someone ,cs please")
            def check(msg):
                return msg.channel == message.channel and msg.content.startswith(',cs')
            try:
                msg = await bot.wait_for('message', check=check, timeout=5)
                await message.channel.send(f'thanks {msg.author.mention} for the ,cs!')
                messages = await message.channel.history(limit=250).flatten()
                for msg in messages:
                    if msg.author == bot.user:
                        try:
                            await msg.delete()
                        except:
                            pass
                break
            except asyncio.TimeoutError:
                pass"""
    if message.author.id == 593921296224747521:
        if 'welcome' in message.content.lower():
            emojis = [e for e in bot.get_guild(1259717095382319215).emojis if e.is_usable()]
            await message.add_reaction(random.choice(emojis))
    await bot.process_commands(message)

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
    await bot.get_guild(guild_id).unban(member.id)
    await ctx.reply(f':white_check_mark:')

    "await ctx.send(f'{member} is not banned! *Maybe you spelled it wrong?*')"

@bot.command(name='ban', help='Bans a user from the server')
@commands.has_any_role(1284509033369305169, 1284508992944476210, 1284508939035349103, 1284508891429736579, 1272930547714232320, 1272963029444595774)
async def ban(ctx, member: discord.User, *, reason=None):
    guild_id = 1259717095382319215
    await ctx.send(f'Looking for {member.name}...')
    try:
        (await bot.get_guild(guild_id)).ban(member, reason=reason)
        await ctx.reply(f':white_check_mark:')
    except:
        await ctx.send(f'{member} is already banned!')
        response = await ctx.prompt(f'Do you want to ban {member.mention} from this server aswell? (y/n)', delete_after=True)
        if response.content.lower() == 'y':
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f':white_check_mark:')

bot.run(config['TOKEN'])