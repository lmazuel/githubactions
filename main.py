#https://discordapp.com/api/oauth2/authorize?client_id=642149752951144468&permissions=8&scope=bot)
#main
import os.path, random, discord, sys, time, asyncio, random
from discord.ext import commands
from discord import member
from discord.ext.commands import Bot
from discord.utils import find


token = os.getenv('BOT_TOKEN')
client = discord.Client()
Client = commands.Bot(command_prefix=">")
prefix = '>'
muted_user = []
trusted_users = "megamaz#4961".split()
number = False
commands = ">censor >uncensor >censored >announce".split()
server_censor = []
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f'{prefix}help'))
    print(f'{client.user.name} is online and usable.')
@client.event
async def on_guild_join(guild):
    print(f"{client.user.name} just joined {guild.name}!")
def check_admin(author):
        if author == client.user:
            return True
        elif ((author).guild_permissions).value == 2146959359:
            return True
        else:
            return False
@Client.command()
async def something(ctx):
    await ctx.send("Test")
def emb_text(emb, description, text, color="normal"):
    global embed_message
    if color == "normal":
        color = 0xe6a100
    if color == "fail":
        color = 0xff0000
    if color == "success":
        color = 0x00cf1f
    if color == "neutral":
        color = 0xfbff00
    embed_message = discord.Embed(title=emb, colour=color)
    embed_message.add_field(name=description, value=text)
    return embed_message

def update_censor(server, AR, _censor=''):
    words = []
    if os.path.exists(f'{server}.txt'):
        with open(f'{server}.txt', 'r') as censor:
            words = censor.read().splitlines()
    else:
        with open(f'{server}.txt', 'w'):
            True

    if AR == 'add':
        if _censor in words:
            return 'fail'
        else:
            with open(f'{server}.txt', 'a') as censor:
                censor.write(f'{_censor}\n')
    elif AR == 'remove':
        if _censor in words:
            words.remove(_censor)
            with open(f'{server}.txt', 'w') as censor:
                words = list(words)
                for x in range(len(words)):
                    censor.write(f'{words[x]}\n')
        else:
            return 'fail'
    elif AR == 'read':
        with open(f'{server}.txt', 'r') as censored:
            words = censored.read().splitlines()
            return words

illegal_char = []
for x in range(255):
    illegal_char.append(chr(x))
@client.event
async def on_message(message):
    for y in range(len(str(message.content).split())):
        if str(message.content).split()[y].lower() in update_censor(str(message.guild), 'read'):
            if message.channel.category_id == None:
                continue
            else:
                await message.delete()
                await message.channel.send(f"{message.author.mention}'s message has been removed for containing a censored word.")
    def check_message(command):
        if message.content == f'{prefix}{command}':
            return True
        else:
            return False
    if message.author == client.user:
        return
    else:
        number = False
        # Normal user commands
        if check_message('help'):
            embed = discord.Embed(title="Commands list", colour=discord.Color(0xe6a100))
            embed.add_field(name=f"Prefix {prefix}", value=f""" This bot is usable by admins only. Normal users will not be able to certain commands.

[] = Required
() = Optional
**Normal user and Admins commands**
{prefix}help
`Gives you this list.`
{prefix}feedback [feedback]
`Gives feedback about the bot. Everything is appreciated!`
{prefix}question [question]
`Any question you have about the bot. If I see it, I'll answer it in #q-and-a`
{prefix}population
`Gives you the population of your server.`

**Admin only list**
{prefix}censor [word]
`Censors a word. Any messages containing that word will be deleted.`
{prefix}uncensor [word]
`Uncensors a word. The word will no longer be censored. It is case sensitive, be sure to put NO CAPITAL LETTERS!!`
{prefix}censored (word)
`Shows a list of the censored words.`
{prefix}announce [Channel ID] [announcement]
`Makes an announcement.`
{prefix}mute [role ID] [user ID]
Still confused? Here is help! https://discord.gg/WkcuE9T""")
            await message.channel.send(embed=embed)
        if f"{prefix}feedback" == message.content[:9]:
            channel = client.get_channel(644001770976051220)
            await message.channel.send(embed=emb_text("Feedback", "*Thanks for the feedback!*", f"""Your feedback `{message.content[10:]}` has been sent to `{channel}` in my support server: https://discord.gg/akJUEwk"""))
            await channel.send(f"From user tag {str(message.author)[-5:]}: `{message.content[10:]}`")
        if f'{prefix}question' == message.content[:9]:
            await message.delete()
            await message.channel.send(embed=emb_text('Your question has been sent.', 'Your question has been sent.', 'Your question has been sent to `#questions` on my support server: https://discord.gg/akJUEwk'))
            channel = client.get_channel(645096217826820117)
            await channel.send(f'Question: {str(message.content)[10:]}')
        if check_message('population'):
            await message.channel.send(f"checking...")
            for y in range(len(client.guilds)):
                if str(message.guild) == str(client.guilds[y].name):
                    await message.channel.send(client.guilds[y].member_count)
                else:
                    continue
        #Admin only commands
        if check_admin(message.author) or not str(message.content).startswith('>censor' or '>censored' or '>uncensor' or '>announce'):
            if message.content.startswith(f"{prefix}censor") and message.content[:9] != f'{prefix}censored':
                if len(message.content) == 7:
                    await message.channel.send(embed=emb_text("Error adding censored word", "Insert a word to censor", 'There was no word to censor.', 'fail'))
                else:
                    for x in range(len(client.guilds)):
                        if client.guilds[x].name == str(message.guild):
                            break
                    if update_censor(str(message.guild), 'add', str(message.content[8:].lower())) == 'fail':
                        await message.channel.send(embed=emb_text("Error adding censored word", "Double", 'Cannot double censor a word.', 'fail'))
                    else:
                        await message.channel.send(embed=emb_text('Success', 'Succesfully added a word', 'A word was successfully added to your censored word list.'))



            if message.content.startswith(f"{prefix}uncensor"):
                update_censor(str(message.guild), 'remove', message.content[10:])
                await message.channel.send(embed=emb_text('Success', 'Successfully removed a word', 'Successfully removed a word from the list.'))
            if message.content.startswith(f'{prefix}censored'):
                if len(message.content) == 9:
                    words = update_censor(str(message.guild), 'read')
                    await message.channel.send(embed=emb_text('List', 'Censored list', f'||{words}||'))
                else:
                    if str(message.content)[10:] in update_censor(str(message.guild), 'read'):
                        await message.channel.send(embed=emb_text('Checking word', 'Word is in list', 'The word you checked is censored', 'success'))
                    else:
                        await message.channel.send(embed=emb_text('Checking word', 'Word is not in list', 'The word you checked is not censored', 'fail'))


            if message.content[:9] == f'{prefix}announce' :
                if len(message.content) == 9:
                    await message.channel.send(embed=emb_text('Error to send announcement', 'Could not send announcement', 'Specify channel ID', 'fail'))
                elif len(message.content) <= 28:
                    await message.channel.send(embed=emb_text('Error to send announcement', 'Could not send announcement', 'Channel ID not long enough' , 'fail'))
                if True:
                    for check_id in range(len(message.content[10:28])):
                        if not message.content[10:28][check_id] in "1 2 3 4 5 6 7 8 9 0".split():
                            await message.channel.send(embed=emb_text('Error to send announcement', 'Could not send announcement', 'Channel ID must contain numbers only', "fail"))
                            number = True
                            break
                        else:
                            continue
                if not number:
                    number = False
                    channel = client.get_channel(int(message.content[10:28]))
                    if channel.guild != message.guild:
                        await message.channel.send(embed=emb_text('Error to send announcement', 'could not send announcement', 'Announcement ID from different server.', 'fail'))
                    else:
                        await message.delete()
                        await channel.send(f'Announcement from {message.author.mention}: {message.content[28:]}')
                        await message.channel.send(embed=emb_text('Success', 'Successfully sent announcement', f'Successfully sent announcement in `#{channel}`'))





        else:
            await message.channel.send(embed=emb_text('Failed', 'Failed to execute command', f"`{message.author}`, you don't have high enough permissions for this."))






        if f'{prefix}shut_bot' == message.content[:9]:
            if str(message.author) in trusted_users:
                if len(message.content) != 9:
                    channel = client.get_channel(643995628623495174)
                    await message.delete()
                    await message.channel.send(embed=emb_text('Success', 'Successfully shut down bot.', 'Bot officially went off.'))
                    await channel.send(f"Bot is going offline for an update. Reason provided: `{message.content[10:]}`")
                    time.sleep(1)
                    await client.logout()
                else:
                    channel = client.get_channel(643995628623495174)
                    await message.delete()
                    await message.channel.send(embed=emb_text('Success', 'Successfully shut down bot.', 'Bot officially went off.'))
                    await channel.send(f"Bot is going offline for an update. No reason provided.")
                    time.sleep(1)
                    await client.logout()


client.run(token)