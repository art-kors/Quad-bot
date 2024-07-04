from typing import Optional
import requests
import discord
from discord import app_commands
from discord.ext import *
import pytube
import time
import json
from random import randint
from req_to_url import *
import os
import hashlib
from spark import *
from fnmatch import *
from pytube.innertube import _default_clients
from collections import deque
import asyncio
import sqlite3

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]
MY_GUILD = discord.Object(id=683739619745071109)  # replace with your guild id
queue = deque([])


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        # self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync()


intents = discord.Intents.all()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command(name='music')
@app_commands.checks.has_permissions(priority_speaker=True)
async def play(interaction: discord.Interaction, link_track : str):
    '''Воспроизводит трек, указанный в параметре link_track. Параметр link_track может содержать ссылку на Youtube-видео или обычный поисковый запрос.
    Использовать данную команду могут только пользователи, обладающие правом "priority speaker".'''
    author = interaction.user
    channel = author.voice.channel
    try:
        await channel.connect()
    except Exception:
        return await interaction.response.send_message('Ошибка! Отключите бота от голосового канала и повторите попытку.')
    if fnmatch(link_track, 'https://www.youtube.com/watch?v=*'):
        pass
    else:
        link_track = search_youtube(link_track)[0][0]
    url_youtube = pytube.YouTube(link_track)
    caption = url_youtube.title
    embed = discord.Embed(
        title=caption,
        description=url_youtube.author,
        colour=discord.Colour(randint(1, 10000))
    )
    await interaction.response.send_message(embed=embed)

    my_itag = url_youtube.streams.filter(only_audio=True)[-1].itag
    mus = url_youtube.streams.get_by_itag(my_itag)
    hash = str(int(hashlib.sha1(link_track.encode("utf-8")).hexdigest(), 16) % (10 ** 8)) # its a name in directory
    print(hash)
    mus.download("tracks", hash+'.mp3')

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./tracks/'+hash+'.mp3'))
    guild = interaction.guild
    print(caption)
    print('/tracks/' + hash + '.mp3')

    guild.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)


#@client.tree.command(name='pics')
#async def pics(interaction: discord.Interaction, tag: str):
#    url = 'https://api.waifu.im/search'
#    params = {
#        'included_tags': [tag],
#        'height': '>=2000'
#    }
#
#    response = requests.get(url, params=params)
#
#    if response.status_code == 200:
#        data = response.json()
#        data = data['images'][0]
#        # Process the response data as needed
#    else:
#        data = 'Not found('
#    await interaction.response.send_message(f'{data["url"]}')


@client.tree.command(name='stop')
@app_commands.checks.has_permissions(priority_speaker=True)
async def stop(interaction: discord.Interaction):
    """Бот останавливает воспроизведение и выходит из голосового канала.
    Использовать данную команду могут только пользователи, обладающие правом "priority speaker"."""
    guild = interaction.guild
    await guild.voice_client.disconnect()
    await interaction.response.send_message(f'Бот вышел из голосового канала')


@client.tree.command(name='pause')
@app_commands.checks.has_permissions(priority_speaker=True)
async def pause(interaction: discord.Interaction):
    """Ставит на паузу воспроизведение трека.
    Использовать данную команду могут только пользователи, обладающие правом "priority speaker"."""
    if interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        await interaction.response.send_message('Пауза')
    else:
        await interaction.response.send_message(
            'У тебя ничего не играет, что ты собираешся поставить на паузу?')


@client.tree.command(name='resume')
@app_commands.checks.has_permissions(priority_speaker=True)
async def resume(interaction: discord.Interaction):
    """Снимает паузу воспроизведение трека.
    Использовать данную команду могут только пользователи, обладающие правом 'priority speaker'."""
    if interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
    else:
        await interaction.response.send_message('Трек уже воспроизводится')


@client.tree.command(name='translate')
async def translate(interaction: discord.Interaction, text: str, from_: str, to: str):
    '''переводит слово/предложение(параметр text) согласно языкам, указанным в команде через параметры _from(с какого языка) и to(на какой язык), за исключением калмыцкого языка.'''
    req = f"https://api.mymemory.translated.net/get?q={text}&langpair={from_}|{to}"

    sp = [req]
    res = ''
    for i in sp:
        response = requests.get(i)
        if response:
            json_response = response.json()
            res = json_response["matches"][0]["translation"]
            print(res)
    await interaction.response.send_message(res)


@client.tree.command(name='rus_to_kalmyk')
async def rtk(interaction: discord.Interaction, text: str):
    '''Перевод с русского на калмыцкий текста, указанного в параметре text. Поддерживается перевод отдельных слов, а не предложений'''
    with open('RUS_TO_KALMYK.json', 'r', encoding='utf-16') as f:  # открыли файл с данными
        base = json.load(f)  # загнали все, что получилось в переменную
    key = ''
    for i in base:
        if text.lower() in i:
            key = i
            break
    print('key:', key)
    ans = base[key]
    await interaction.response.send_message(ans)


@client.tree.command(name='kalmyk_to_rus')
async def ktr(interaction: discord.Interaction, text: str):
    '''Перевод с калмыцкого на русский текста, указанного в параметре text'''
    with open('KALMYK_TO_RUS.json', 'r', encoding='utf-16') as f:  # открыли файл с данными
        base = json.load(f)  # загнали все, что получилось в переменную

    if text.lower() not in text:
        await interaction.response.send_message('Не нашёл слово')
    else:
        print(base[text.lower()])
        data = base[text.lower()].split('\n')
        if data[-1] == '':
            data.append('Янзнь уга (примеров нет)')
        ans = ''
        for i in range(len(data)):
            if data[i] != '':
                ans += data[i] + '\n'
        await interaction.response.send_message(ans)

@client.tree.command(name='kalmyk_letters')
async def kalmyk_letters(interaction: discord.Interaction):
    '''выводит калмыцкие буквы'''
    await interaction.response.send_message('Ə ә Һ һ Җ җ Ң ң Ө ө Ү ү')

@client.tree.command(name='give_role')
@app_commands.checks.has_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, user: discord.Member, role: discord.Role, time: int, *, reason: str):
    '''Выдает роль(параметр role) пользователю (параметр user) на время (параметр time) (в минутах). reason - причина выдачи роли(обычно используется для выдачи mute-роли).
    Использовать данную команду могут только пользователи, обладающие правом "mute members".'''
    # author = interaction.user.guild_permissions.mute_members
    guild = interaction.guild

    emb = discord.Embed(title='✅Получилось',
                        description=f"Пользователю {user} выдали {role.name}!\nВремя пребывания на данной роли: {time} минут\nПричина выдачи роли: {reason}!",
                        colour=discord.Color.green())
    emb.set_footer(text='Действие выполнено модератором/админом - ' + interaction.user.name,
                   icon_url=interaction.user.display_avatar)
    await interaction.response.send_message(embed=emb)
    await interaction.response.message.delete()
    await user.add_roles(role)  # выдает мьют роль
    await asyncio.sleep(
        time * 60)  # ждет нужное кол-во секунд умноженных на 60(вы выдаете мут на минуты. Допустим time = 10, то вы выдали мут на 10 минут)
    await user.remove_roles(role)  # снимает мьют роль


@client.tree.command(name='filter_link')
@app_commands.checks.has_permissions(administrator=True)
async def filter_param(interaction: discord.Interaction, on: bool, autoban_time: int, cnt_warn: int):
    '''Фильтр, не допускающий ссылок в чате(действует на весь сервер).
    Параметр on - вкл/выкл фильтра.
    Параметр autoban_time - бан на какой срок(в минутах).
    Параметр cnt_warn - сколько предупреждений нужно выдать перед баном.
    Люди, у которых есть право "embed links" на сервере, не будут получать варны и баны.
    Использовать данную команду могут только администраторы.'''
    # author = interaction.user.guild_permissions.mute_members

    params = [True, int(on), int(autoban_time), cnt_warn]
    guild = interaction.guild.id
    connection = sqlite3.connect('servers.db')
    cursor = connection.cursor()
    guilds = list(map(lambda x: x[0], cursor.execute('SELECT guild_id FROM guild_settings').fetchall()))
    if guild in guilds:
        cursor.execute('UPDATE guild_settings SET automute=?, automute_time=?, count_warn_to_ban=? WHERE guild_id = ?',
                       (int(on), int(autoban_time), cnt_warn, guild))
    else:
        cursor.execute(
            'INSERT INTO guild_settings (guild_id, warn_links, automute, automute_time, count_warn_to_ban) VALUES (?, ?, ?, ?, ?)',
            (guild, *params))
    connection.commit()
    connection.close()
    await interaction.response.send_message('сработало')


@client.tree.command(name='rtm')
async def rtm(interaction: discord.Interaction, text: str):
    '''Перевод с русского на "морзянку" текста, указанного в параметре text'''
    res = rus_to_morze(text)
    await interaction.response.send_message(text)


@client.tree.command(name='etm')
async def etm(interaction: discord.Interaction, text: str):
    '''Перевод с английского на "морзянку" текста, указанного в параметре text'''
    res = encode_to_morse(text)
    await interaction.response.send_message(text)

@client.tree.command(name='mte')
async def mte(interaction: discord.Interaction, text: str):
    '''Перевод с "морзянки" на английский текста, указанного в параметре text'''
    res = decode_to_morse(text)
    await interaction.response.send_message(text)

@client.tree.command(name='mtr')
async def mtr(interaction: discord.Interaction, text: str):
    '''Перевод с "морзянки" на русский текста, указанного в параметре text'''
    res = morze_to_rus(text)
    await interaction.response.send_message(text)

@client.tree.command(name='help')
async def help(interaction: discord.Interaction, text: str):
    '''Гайд на каждую команду'''
    res = '''
    МУЗЫКА (Использовать данные команды могут только пользователи, обладающие правом 'priority speaker'):
    
    play - Воспроизводит трек, указанный в параметре link_track. Параметр link_track может содержать ссылку на Youtube-видео или обычный поисковый запрос.
    stop - Бот останавливает воспроизведение и выходит из голосового канала.
    pause - Использовать данную команду могут только пользователи, обладающие правом "priority speaker".
    resume - Снимает паузу воспроизведение трека.
    
    Администрирование:
    give_role - Выдает роль(параметр role) пользователю (параметр user) на время (параметр time) (в минутах). reason - причина выдачи роли(обычно используется для выдачи mute-роли).
    Использовать данную команду могут только пользователи, обладающие правом "mute members".
    filter_param - Фильтр, не допускающий ссылок в чате(действует на весь сервер).
    Параметр on - вкл/выкл фильтра.
    Параметр autoban_time - бан на какой срок(в минутах).
    Параметр cnt_warn - сколько предупреждений нужно выдать перед баном.
    Люди, у которых есть право "embed links" на сервере, не будут получать варны и баны.
    Использовать данную команду могут только администраторы
    Переводчики:
    translate - переводит слово/предложение(параметр text) согласно языкам, указанным в команде через параметры _from(с какого языка) и to(на какой язык), за исключением калмыцкого языка.
    rus_to_kalmyk - Перевод с русского на калмыцкий текста, указанного в параметре text. Поддерживается перевод отдельных слов, а не предложений.
    kalmyk_to_rus - Перевод с калмыцкого на русский текста, указанного в параметре text. Поддерживается перевод отдельных слов, а не предложений.
    "Морзянка":
    etm - Перевод с английского на "морзянку" текста, указанного в параметре text.
    mte - Перевод с "морзянки" на английский текста, указанного в параметре text.
    rtm - Перевод с русского на "морзянку" текста, указанного в параметре text.
    mtr - Перевод с "морзянки" на русский текста, указанного в параметре text.
    '''
    await interaction.response.send_message(text)


@client.event
async def on_message(message):
    guild = message.guild.id
    user_id = message.author.id
    user = message.author
    roles = user.roles
    link_perm = False
    for i in roles:
        if i.permissions.embed_links:
            print('право отправлять ссылки чееееек', i.permissions.embed_links)
            print(i.name)
            link_perm = True

    connection = sqlite3.connect('servers.db')
    cursor = connection.cursor()
    print(fnmatch(message.content, 'https://*'), link_perm)
    if fnmatch(message.content, 'http://*') or fnmatch(message.content, 'https://*') and not link_perm and \
            list(cursor.execute(f'SELECT automute FROM guild_settings WHERE guild_id = {guild}').fetchall())[0][0]:

        print(guild)
        ban_time = \
        list(cursor.execute(f'SELECT automute_time FROM guild_settings WHERE guild_id = {guild}').fetchall())[0][0]
        cnt_warn = \
        list(cursor.execute(f'SELECT count_warn_to_ban FROM guild_settings WHERE guild_id = {guild}').fetchall())[0][0]
        warn_links = \
        list(cursor.execute(f'SELECT warn_links FROM guild_settings WHERE guild_id ={guild}').fetchall())[0][0]
        try:
            cnt_warn_user = list(cursor.execute('SELECT cnt_warn FROM users WHERE user_id=? AND guild_id = ?',
                                                (user_id, guild)).fetchall())[0][0] + 1
        except Exception:
            cursor.execute(
                f'INSERT INTO users (user_id, guild_id, cnt_warn, banned) VALUES ({user_id}, {guild}, {0}, {False})')
            cnt_warn_user = 1
        cursor.execute(f'UPDATE users SET cnt_warn = {cnt_warn_user} WHERE guild_id={guild} AND user_id={user_id}')
        connection.commit()
        if warn_links:
            await message.channel.send(
                f'Вы получили предупреждение! {cnt_warn_user}/{cnt_warn} предупреждений на сервере - бан на {ban_time} минут!')
        print(cnt_warn_user, cnt_warn)
        if cnt_warn <= cnt_warn_user:
            cursor.execute(f'UPDATE users SET cnt_warn = {0} WHERE guild_id={guild} AND user_id={user_id}')
            connection.commit()
            await message.channel.send('Бан!', delete_after=10)

            guild = message.guild
            member = await guild.fetch_member(user_id)
            await member.ban(reason='ссылки в чате', delete_message_days=1)
            await asyncio.sleep(ban_time * 60)
            await member.unban()


client.run('MTI1Nzc0OTIyODk4MjM3MDM0NA.GJB6Jj.iDKG2AxbXiVxZK5oTbJNSlYGzUvwkH65Av2PuE')