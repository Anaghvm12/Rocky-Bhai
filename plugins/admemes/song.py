

from pyrogram import Client, filters

import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
import time

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------

@Client.on_message(filters.command("song") & ~filters.channel & ~filters.edited)
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`🎻𝖥𝗂𝗇𝖽𝗂𝗇𝗀 𝖸𝗈𝗎𝗋 𝖲𝗈𝗇𝗀🎶.....`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[ᴍᴀɢɴᴜs ᴛɢ ᴍᴜsɪᴄ]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**<b>𝖨 𝖺𝗆 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 𝖱𝖾𝗌𝗎𝗅𝗍 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 ❤️.𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗇𝗈𝗍𝗁𝖾𝗋 𝖲𝗈𝗇𝗀 𝖮𝗋 𝖴𝗌𝖾 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖶𝗈𝗋𝖽💕!</b>**')
            return
    except Exception as e:
        m.edit(
            "**𝖤𝗇𝗍𝖾𝗋 𝗌𝖲𝗈𝗇𝗀 𝖭𝖺𝗆𝖾 𝖶𝗂𝗍𝗁 𝖢𝗈𝗆𝗆𝖺𝗇𝖽💕**❗\n𝖥𝗈𝗋 𝖤𝗑𝖺𝗆𝗉𝗅𝖾: `/song Alone Marshmellow`"
        )
        print(str(e))
        return
    m.edit("`𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀...🎻`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎹 <b>𝖳𝗂𝗍𝗅𝖾:</b> <a href="{link}">{title}</a>\n🎙️ <b>𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:</b> <code>{duration}</code>\n🎵 <b>𝖵𝗂𝖾𝗐𝗌:</b> <code>{views}</code>\n🎻 <b>𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒:</b> {message.from_user.mention()} \n🎶 <b>𝖴𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝖡𝗒: @Universal_MoviesZ</b> 👑'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**𝖠𝗇 𝖤𝗋𝗋𝗈𝗋 𝖮𝖼𝖼𝗎𝗋𝖾𝖽 𝖯𝗅𝖾𝖺𝗌𝖾 𝖱𝖾𝗉𝗈𝗋𝗍 𝖳𝗁𝗂𝗌 𝗍𝗈 @MagnusTG !!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
