import os
from datetime import datetime
from typing import Final, Sequence

import discord
from discord import Intents, Client, Message, Role
from dotenv import load_dotenv

from responses import get_verification

# LOAD TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)
bot_log: discord.TextChannel = ...
bot_log_channel_id: int = 1242232223147622441


# VERIFICATION FUNCTIONALITY
async def verify(message: Message, user_info: str) -> None:
    '''
    Using a student's first name, last name, and uin, they are either verified or unverified
    depending on whether they are part of the verified students list.
    :param message: Should be the user's First Name, Last Name, and UIN as type Message
    :param user_info: Should be the user's First Name, Last Name, and UIN as type str
    :return: None
    '''
    if not user_info:
        print('(Message was empty because intents were not enabled probably)')
        return
    # if is_private := user_message[0] == '?':
    #     user_message = user_message[1:]
    try:
        response: str = get_verification(user_info)
        member: discord.Member = message.author
        guild_id: int = message.guild.id
        guild_roles: Sequence[Role] = client.get_guild(guild_id).roles
        verified_role: discord.Role = discord.utils.get(guild_roles, name='Verified Member')
        unverified_role: discord.Role = discord.utils.get(guild_roles, name='Unverified Member')
        split_name: list[str] = user_info.split(' ')

        if response == 'Verified!':
            await remove_role(member, unverified_role)
            await add_role(member, verified_role)
            await set_nick(member, (split_name[0].title(), split_name[1].title()))
        elif response == 'NOT Verified!':
            await remove_role(member, verified_role)
            await add_role(member, unverified_role)
            await set_nick(member, (split_name[0].title(), split_name[1].title()))
        await message.channel.send(response, silent=True)
        await message.delete()
    except Exception as e:
        print(e)
        await log_event(f'Could not verify [{message.author}] due to ``{str(e)[str(e).rindex(":") + 2:]}``')


# BOT LOGIC TO CHANGE MEMBER'S DETAILS
async def set_nick(user: discord.Member, name: tuple[str, str]) -> None:
    '''
    Sets the server nickname for a user.
    :param user: The member who is getting their nickname changed
    :param name: The first and last name of the user which will be their new server nickname
    :return: None
    '''
    nickname = ' '.join(name)
    print(f'Changing {user} nickname to {nickname}')
    try:
        await user.edit(nick=nickname)
        await log_event(f'Changing [{user}] nickname to "{nickname}"')
    except Exception as e:
        await log_event(
            f'Could not change [{user}] nickname to "{nickname}" due to ``{str(e)[str(e).rindex(":") + 2:]}``')


async def add_role(user: discord.Member, role: discord.Role) -> None:
    '''
    Adds a role to a discord member.
    :param user: The discord member which is receiving the role
    :param role: The discord role which the user is receiving
    :return: None
    '''
    if role not in user.roles:
        try:
            await user.add_roles(role)
            await log_event(f'"{role}" role added to [{user}]')
        except Exception as e:
            await log_event(f'"{role}" could not be added to [{user}] due to ``{str(e)[str(e).rindex(":") + 2:]}``')
    else:
        await log_event(f'Tried to add role "{role}" to [{user}], but they already had that role')


async def remove_role(user: discord.Member, role: discord.Role) -> None:
    '''
    Removes a ``role`` from a discord ``member``.
    :param user: The discord member which is having the role removed
    :param role: The discord role which is being removed from the user
    :return: None
    '''
    if role in user.roles:
        try:
            await user.remove_roles(role)
            await log_event(f'"{role}" role removed from [{user}]')
        except Exception as e:
            await log_event(
                f'"{role}" role could not be removed from [{user}] due to ``{str(e)[str(e).rindex(":") + 2:]}``')
    else:
        await log_event(f'Tried to remove role "{role}" from [{user}], but they never had that role')


# HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    '''
    Whenever a user sends a ``message`` to any ``channel``, this function is called.
    The bot will respond differently depending on the ``channel``.
    :param message: The discord message sent by a user
    :return: None
    '''
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    if channel == '✅︱verification':
        await verify(message, user_message)
    elif user_message == '!close':
        await message.delete()
        if username == 'tsmith422':
            await disconnect()
        else:
            await log_event(f'[username] attempted to shut me down')


# LOG IMPORTANT EVENTS TO BOT-ALERTS
async def log_event(event: str) -> None:
    '''
    Sends a message of significant bot ``events`` to the log.
    :param event: String of the event we want to log
    :return: None
    '''
    current_time: datetime = datetime.now()
    global bot_log
    await bot_log.send(f'>>> {event} \n``{current_time:[%m.%d.%y %H:%M]}``', silent=True)


# HANDLING STARTUP FOR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

    global bot_log
    bot_log = client.get_channel(bot_log_channel_id)

    await log_event(f'### [{str(client.user)[:-5]}] is now running!')


# HANDLING DISCONNECTIONS
@client.event
async def on_disconnect() -> None:
    print('Disconnecting from client')
    try:
        await log_event(f'[{str(client.user)[:-5]}] is now disconnected from client')
    except Exception as e:
        print(e)


async def disconnect() -> None:
    await log_event(f'### [{str(client.user)[:-5]}] is now disconnected from client')
    await client.close()


# MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
