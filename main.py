import json, discord, datetime, random, asyncio, aiohttp, time
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

time = time.time()

@bot.event
async def on_message(message):
    if message.channel.id == 1266199316742275214:
        if message.author.id == 814226043924643880:
            thread = await message.channel.create_thread(name=f"{message.created_at.strftime('%d-%m-%Y %H:%M:%S')} {message.author.name}", message=message)

            async def create_summary():
                """Create a summary of the given thread and post it at the end."""
                await asyncio.sleep(3 * 60 * 60)
                messages = await thread.history(limit=100, oldest_first=True).flatten()
                if len(messages) > 10:
                    content = ' '.join(msg.clean_content for msg in messages)
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            "https://api.aicloud.sensory.ai/key/value/summarize",
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": "Basic OGFmZmU1NmItYmU2Ni00NjIyLWE0MjQtODkwMmM2MDk0MzlkOjE2MzQyNzY0NTU3NQ=="
                            },
                            data=json.dumps({"text": content})
                        ) as response:
                            summary = (await response.json())["summary"]
                            message = await thread.send(f"Thread Summary: {summary}")
                            await message.pin()
            #asyncio.create_task(create_summary())
    
    elif any(word in message.content.lower() for word in words):
    
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
    elif message.author.id == 593921296224747521:
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
        recent_changes.append('<:upvote:1269483637892714599>')
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
        recent_changes.append('<:downvote:1279377401792434258>')
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

@bot.command(name='statistics', aliases=['stats', 'ut', 'info'], help='Shows some stats of the bot')
async def statistics(ctx):
    embed = discord.Embed(title='Uptime', color=discord.Color.green())
    embed.add_field(name='Ping', value=f'{int(bot.latency * 1000)}ms', inline=True)
    embed.add_field(name='Member Count', value=f'{sum(g.member_count for g in bot.guilds)}', inline=False)
    embed.add_field(name='Server Count', value=f'{len(bot.guilds)}', inline=False)
    await ctx.send(embed=embed)

@bot.command(name='servers', help='Displays all servers the bot is connected to and their member counts')
async def servers(ctx):
    embed = discord.Embed(title='Servers', color=discord.Color.green())
    for guild in bot.guilds:
        embed.add_field(name=guild.name, value=f'{guild.member_count} members', inline=False)
    await ctx.send(embed=embed)

@bot.command(name='ping', help='Pings the bot')
@commands.is_owner()
async def ping(ctx):
    await ctx.reply(f'Pong! {int(bot.latency * 1000)}ms')

@bot.command(name='echo', help='Echoes back what you said')
@commands.is_owner()
async def echo(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(name='clear', help='Clears a certain amount of messages')
@commands.is_owner()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error



bot.run(config['TOKEN'])