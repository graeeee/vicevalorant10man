import asyncio
import discord
import myToken
import random

from discord.ext import commands
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import bot
from discord.ext.commands import (command, cooldown, CommandOnCooldown)


# loads of vars we'll need to persist
bot = commands.Bot(command_prefix=myToken.prefix,
                   description=myToken.description)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="#roles to join 10mans"))
    print("Bot is online and working somewhat")

ourServer = None
inProgress = False
queueUsers = []
firstCaptain = None
secondCaptain = None
teamOne = []
teamTwo = []
currentPickingCaptain = ""
pickNum = 1
team1ChannelId = 698323152836493312
team2ChannelId = 698323212773228584
serverName = myToken.guildID


async def queueUp(ctx):
    
    
    
    # we received a message
    # modifying these globals
    global inProgress
    global queueUsers
    global firstCaptain
    global secondCaptain
    global teamOne
    global teamTwo
    global pickNum

    # extract the author and message from context.
    author = ctx.author
    message = ctx.message

    # make sure they're using the bot setup channel
    if(message.channel.id != myToken.setupChannelId):
        # if they aren't using an appropriate channel, return
        return

    # queue command
    rolequeue = discord.utils.find(lambda r: r.name == 'lastgame', ctx.message.guild.roles)
    if (inProgress == False and len(queueUsers) < 10):
        # check if they are already queued
        if(author in queueUsers or rolequeue in author.roles):
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = ("Error joining queue.")
                embed.description = (author.mention + ", you are already in the queue either through a command,\nd or through the 10man last game voice channel.")
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
        #actually queueing up
        else:
            # add them to the queue list and send a message
            queueUsers.append(author)
            #if the first person joins the queue, send notification as well as telling people how to join
            if(len(queueUsers) == 1):
                bot_avatar = bot.user.avatar_url
                await ctx.send("<@&796195408920444951>")
                embed = discord.Embed()
                embed.title = (str ( len(queueUsers)) + " player is now in queue.")
                embed.description = (author.mention + " has joined queue.\n\nNeeded users: **" + str(10 - len(queueUsers)) + "**")
                embed.add_field(name=f"Want to join?", value=f"type !q or !queue to join the 10man!")
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
            elif(len(queueUsers) == 10):
                # we have 10 queue users, now need captains
                await ctx.channel.send(" ".join(sorted(str(x.mention) for x in queueUsers)) + " ")
                inProgress = True
                firstCaptain = queueUsers[random.randrange(len(queueUsers))]
                secondCaptain = queueUsers[random.randrange(len(queueUsers))]
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.add_field(name="**10man Queue Filled**",
                                value=f"The queue has reached 10 players, Please join the 10man Queue channel as soon as possible.",
                                inline=False)
                embed.add_field(name="**Captains**", value=f'{firstCaptain.mention} and {secondCaptain.mention}', inline=False)
                
                embed.add_field(name="Captain Selection",
                                value=f'{firstCaptain.mention} has been chosen for first pick and will add players to join the party.\n{secondCaptain.mention} has been chose for map pick and side pick.',
                                inline=False)
                embed.set_thumbnail(url=bot_avatar)
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
                inProgress = False
                queueUsers = []
                teamOne = []
                teamTwo = []
                firstCaptain = None
                secondCaptain = None
                pickNum = 1
                
            elif(len(queueUsers) != 0):
                #player joined queue
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = (str( len(queueUsers)) + " player(s) are now in queue.")
                embed.description = (author.mention + " has joined queue.\n\nNeeded Users: **" + str(10 - len(queueUsers)) + "**")
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
            elif(len(queueUsers) >= 11):
                #player joined queue
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = (str(10 + len(queueUsers)) + " player(s) are now in priority queue.")
                embed.description = (author.mention + " has joined priority queue.\n\n" + author.mention + " now has the " + str(10 + len(queueUsers)) + "spot in priority queue.")
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
            return


async def notqueue(ctx):
    global queueUsers
    author = ctx.author
    bot_avatar = bot.user.avatar_url
    try:
        queueUsers.remove(author)
        # unqueue message
        embed = discord.Embed()
        embed.title = (str ( len(queueUsers)) + " player(s) are now in queue. (!unq)")
        embed.description = (author.mention + " has left queue\n\nNeeded users: **" + str(10 - len(queueUsers)) + "**")
        embed.color = (0xF8C300)
        embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
        await ctx.send(embed=embed)
    except ValueError:
        #if they havent joined queue and try to unqueue, leave messsage 
        return


#remove user from queue
@bot.command(description="Removes user from queue")
@commands.has_role("Hosts")
async def queuekick(ctx, member: discord.Member):
    guild = ctx.guild

    queueUsers.remove(member)
    await ctx.send(f"{member} has been removed from queue. (kicked by host)")

    return
#same command, just qkick instead of queuekick
@bot.command(description="Removes user from queue")
@commands.has_role("Hosts")
async def qkick(ctx, member: discord.Member):
    guild = ctx.guild
    
    queueUsers.remove(member)
    await ctx.send(f"{member} has been removed from queue. (kicked by host)")

    return

    

        
@bot.event
async def on_queue():
    global ourServer
    global team1VoiceChannel
    global team2VoiceChannel

    team1VoiceChannel = bot.get_channel(team1ChannelId)
    team2VoiceChannel = bot.get_channel(team2ChannelId)
    print('------')
    print('Logged in as {} with id {}'.format(bot.user.name, bot.user.id))
    print('VC1 Name is {}\nVC2 Name is {}'.format(
        team1VoiceChannel, team2VoiceChannel))
    print('------')
    # loop over all the servers the bots apart


@bot.command()
async def queue(ctx):
    await queueUp(ctx)
    return


@bot.command()
async def q(ctx):
    await queueUp(ctx)
    return

@bot.command()
async def unqueue(ctx):
    await notqueue(ctx)
    return


@bot.command()
async def unq(ctx):
    await notqueue(ctx)
    return

@bot.command()
async def qlist(ctx):
    await queuelist(ctx)
    return



@bot.command()
@commands.has_role("Hosts")
async def queuereset(ctx):
    
    global inProgress
    global queueUsers
    global firstCaptain
    global secondCaptain
    global teamOne
    global teamTwo
    global pickNum
    

    inProgress = False
    queueUsers = []
    teamOne = []
    teamTwo = []
    firstCaptain = None
    secondCaptain = None
    pickNum = 1
    bot_avatar = bot.user.avatar_url
    author = ctx.author
    embed = discord.Embed()
    embed.title = ("Current queue has been reset")
    embed.description = (author.mention + " has reset the queue. to join the new queue, type !q or !queue.")
    embed.color = (0xF8C300)
    embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
    await ctx.send(embed=embed)
    
    return

@bot.command()
@commands.has_role("Hosts")
async def qreset(ctx):
    await queuereset(ctx)
    return

@bot.command()
async def queuelist(ctx):
    global queueUsers
    if (len(queueUsers) == 0):
        
        bot_avatar = bot.user.avatar_url
        embed = discord.Embed()
        embed.title = ("Current Queue (" + str ( len(queueUsers)) + " players)")
        embed.description = ("Queue is empty, type !q or !queue to join. \n ")
        embed.color = (0xF8C300)
        embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
        await ctx.send(embed=embed)
    else:
        bot_avatar = bot.user.avatar_url
        embed = discord.Embed()
        embed.title = ("Current Queue (" + str ( len(queueUsers)) + " players) \n")
        embed.description = (" \n ".join(sorted(str(x.mention) for x in queueUsers)))
        embed.color = (0xF8C300)
        embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
        await ctx.send(embed=embed)
    return
@bot.command()
async def test(ctx):
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = ("10man Setup Finished")
                embed.description = ('''The teams are now made and have been moved to their correct teams.\n
                Team 1: ''' + ", ".join(str(x.name) for x in teamOne) + '''
                
                Team 2: ''' + ", ".join(str(x.name) for x in teamTwo) + '''
                \n*Any Questions? DM* <@819027518279122994> *or message a host or staff member!*''')
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
				
@bot.command(description="Removes user from queue")
@commands.has_role("Hosts")
async def qadd(ctx, member: discord.Member):
    guild = ctx.guild
     
    queueUsers.append(member)
    await ctx.send(f"{member} has been added to queue.")


@bot.command(description="testing if this works")
async def testroleone(msg):
    guild = msg.guild
    author = msg.author
    message = msg.message
    channel = msg.channel
    role = discord.utils.find(lambda r: r.name == '10 Man', msg.message.guild.roles)
    roletwo = discord.utils.find(lambda r: r.name == '10 Man (muted)', msg.message.guild.roles)

    if role in author.roles or roletwo in author.roles:
        await msg.send(f'Yes')
    else:
        await msg.send(f"No")
    return


@bot.command()
@commands.has_role("Hosts")
@cooldown(1, 1800, BucketType.guild) #this is the cooldown timer 300 = seconds of cooldown
async def qmention(ctx):
    author = ctx.author
    guild = ctx.guild 
    bot_avatar = bot.user.avatar_url
    await ctx.send("<@&796195408920444951>")
    embed = discord.Embed()
    embed.title = ("Queue Re-Mention")
    embed.description = (str(len(queueUsers)) + " players are currently in queue\n\nNeeded users: **" + str(10 - len(queueUsers)) + "**<:blank:819404890744160316>")
    embed.add_field(name=f"Want to join?", value=f"type !q or !queue to join the 10man!")
    embed.color = (0xF8C300)
    embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
    await ctx.send(embed=embed)

@bot.command()
async def test2(ctx):
                o = "<:viceline:819753141557526539>"
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = ("React to this message with your region of choice")
                embed.description = (o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + "\n\n> <:vicena:819686230227681300> <:viceminus:819753873224106065> North America\n\n> <:viceeu:819687278414528548> <:viceminus:819753873224106065> Europe\n\n*Not all regions are here, choose your prefered.*\n <:blank:819404890744160316>")
                embed.color = (0xF8C300)
                await ctx.send(embed=embed)

@bot.command()
async def test3(ctx):
                o = "<:viceline:819753141557526539>"
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = ("React to gain or remove access to the 10man channels")
                embed.description = (o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o +"\n\n> <:ViceValorant:805351565774422096> <:viceminus:819753873224106065> Gain access to 10mans\n\n> <:ViceValorant:805351565774422096> <:viceminus:819753873224106065> Gain access to 10mans, but have muted role\n\n*Muted role with stop you from getting notifications.\n if you want notifications, react with the valorant logo.*\n <:blank:819404959111970816>")
                embed.color = (0xF8C300)
                await ctx.send(embed=embed)

@bot.command()
async def test4(ctx):
                o = "<:viceline:819753141557526539>"
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = ("React to get notifications for the server or 10man notifications")
                embed.description = (o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + "\n\n> :bell: <:viceminus:819753873224106065> Get important general notifications\n\n> <:vice:805351444713701397> <:viceminus:819753873224106065> Get important 10man notifications\n\n*@everyone will still be used for important information.*\n <:blank:819404890744160316>")
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)
            
@bot.command()
async def test5(ctx):
                o = "<:viceline:819753141557526539>"
                bot_avatar = bot.user.avatar_url
                embed = discord.Embed()
                embed.title = ("React to get yoru ran")
                embed.description = (o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + o + "\n\n> :bell: <:viceminus:819753873224106065> Get important general notifications\n\n> <:vice:805351444713701397> <:viceminus:819753873224106065> Get important 10man notifications\n\n*@everyone will still be used for important information.*\n <:blank:819404890744160316>")
                embed.color = (0xF8C300)
                embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar,)
                await ctx.send(embed=embed)


@bot.command(description="testing if this works")
async def testrole(msg):
    guild = msg.guild
    author = msg.author
    message = msg.message
    channel = msg.channel
    role = discord.utils.find(lambda r: r.name == '10 Man', msg.message.guild.roles)
    roletwo = discord.utils.find(lambda r: r.name == '10 Man (muted)', msg.message.guild.roles)

    if role in author.roles or roletwo in author.roles:
        await msg.send(f'Yes')
    else:
        await msg.send(f"No")
    return





import logging
logging.basicConfig(level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("logs.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

# Vice ids
#queue_na_role_id = 719620287129321502
#queue_eu_role_id = 719620470621863956
lastgame_role_id = 719625580596691054
lastgame_role_ready_id = 719625720581718055
tenman_role_id = 796195408920444951
captain_role_id = 698343215119597669
#queue_na_id = 698323056484941914
#queue_eu_id = 698323700025524345
queue_last_id = 824104178175180830
queue_teams_ids = [820097295209988098, 698323212773228584,
                   698323152836493312, 820097306488733717]
channel_id = 698328368676077698


@bot.event
async def on_voice_state_update(member, before, after):
    if tenman_role_id in [x.id for x in member.roles]:

        # Member joined a channel
        if before.channel is None and after.channel is not None:

            # Queue last
            if after.channel.id == queue_last_id:
                await check_ready(member, lastgame_role_id, after)

        # Member left a channel
        elif before.channel is not None and after.channel is None:

            # Queue teams
            if before.channel.id in queue_teams_ids:
                await remove_role(member, lastgame_role_id)

            # Queue last
            elif before.channel.id == queue_last_id:
                await remove_role(member, lastgame_role_id)

        # Member switched channels
        elif before.channel.id != after.channel.id:


            # Left queue last
            if before.channel.id == queue_last_id:
                await remove_role(member, lastgame_role_id)

            # Left queue teams
            elif before.channel.id in queue_teams_ids:
                await remove_role(member, lastgame_role_id)

            # Joined queue teams
            elif after.channel.id in queue_teams_ids:
                await add_role(member, lastgame_role_id)

            # Joined queue last
            if after.channel.id == queue_last_id:
                await check_ready(member, lastgame_role_id, after)


def get_role(member, role_id):
    return discord.utils.get(member.guild.roles, id=role_id)


def member_name(member):
    return f'{member.nick} - {member.mention}'


async def remove_role(member, role_id):
    logging.info(f'Attempting to remove role \"{role_id}\" from member \"{member_name(member)}\"')
    role = get_role(member, role_id)
    await member.remove_roles(role)


async def add_role(member, role_id):
    logging.info(f'Attempting to add role \"{role_id}\" to member \"{member_name(member)}\"')
    role = get_role(member, role_id)
    await member.add_roles(role)


async def check_ready(member, role_id, after):
    logging.info(f'Member \"{member_name(member)}\" joined queue: \"{after.channel.name}\"')
    role = get_role(member, role_id)
    await member.add_roles(role)

    
    if len(after.channel.members) == after.channel.user_limit:
        captains = await choose_captains(role, after)

        channel = bot.get_channel(channel_id)
        bot_avatar = bot.user.avatar_url
        embed = discord.Embed()
        embed.set_thumbnail(url=bot_avatar)
        embed.add_field(name="**Queue Filled**",
                        value=f'{after.channel.name} has reached 10 players. Captains will start adding players on VALORANT to fill the party.',
                        inline=False)
        embed.add_field(name="**Captains**", value=f'{captains[0].mention} and {captains[1].mention}', inline=False)

        if random.randint(0, 1):
            captains.reverse()
        
        embed.add_field(name="**Captain Selections**",
                        value=f'{captains[0].mention} has been chosen for first pick and will add players to join the party.\n{captains[1].mention} has been chosen for map and side.',
                        inline=False)
        embed.set_footer(text='Vice Valorant 10mans/Scrims', icon_url=bot_avatar)
        embed.color = (0xF8C300)
        await channel.send(content=f'{role.mention}', embed=embed)


async def choose_captains(role, after):
    logging.info(f'Attempting to choose captains from the members of the role \"{role.id}\"')
    members = after.channel.members
    members_copy = list(members)
    captain_roles = []
    for member in members:
        if any([captain_role_id == x.id for x in member.roles]):
            captain_roles.append(member)
            members_copy.remove(member)

    num_captains = len(captain_roles)
    if num_captains == 0:
        return random.sample(members, 2)
    elif num_captains == 1:
        captains = list(captain_roles)
        captains.append(random.choice(members_copy))
        return captains
    else:
        return random.sample(captain_roles, 2)
bot.run(myToken.token)
