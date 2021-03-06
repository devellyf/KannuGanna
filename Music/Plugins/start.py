import yt_dlp
from pyrogram import filters
from pyrogram import Client
from Music import app, SUDOERS, BOT_ID, BOT_USERNAME, OWNER
from Music import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME
from Music.MusicUtilities.helpers.inline import start_keyboard, personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.filters import command
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from Music.MusicUtilities.database.chats import (get_served_chats, is_served_chat, add_served_chat, get_served_chats)
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Music.MusicUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo)

def start_pannel():  
    buttons  = [
            [
                InlineKeyboardButton(text="π Commands Menu", url="http://telegra.ph/ππ¬ππ«π¬-ππ¨π¦π¦ππ§ππ¬-11-30")
            ],
            [ 
                InlineKeyboardButton(text="π¨Official Channel", url="https://t.me/kannu_op"),
                InlineKeyboardButton(text="π¨Support Group", url="https://t.me/XdTeleban")
            ],
    ]
    return "π  **This is kannuc Music Bot**", buttons

pstart_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("π Sα΄α΄α΄α΄Ι΄ Mα΄ π", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ], 
                [InlineKeyboardButton("π§° Cα΄α΄α΄α΄Ι΄α΄κ± π§°", url=f"http://telegra.ph/ππ¬ππ«π¬-ππ¨π¦π¦ππ§ππ¬-11-30")],
                [
                    InlineKeyboardButton(
                        "π’ Uα΄α΄α΄α΄α΄κ± π’", url=f"https://t.me/kannu_op"), 
                    InlineKeyboardButton(
                        "π¬ Sα΄α΄α΄α΄Κα΄ π¬", url=f"https://t.me/XdTeleban")
                ],
                [ InlineKeyboardButton("π§βπ» Sα΄α΄Κα΄α΄ Cα΄α΄α΄ π§βπ»", url=f"https://telegra.ph/file/ba46771a8905abacbe0cf.jpg"),]

            ]
        )
welcome_captcha_group = 2
@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(f"**__Not in allowed chats.__**\n\nMusic Private is only for allowed chats. Ask any Sudo User to allow your chat.\nCheck Sudo Users List [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)")
        return await app.leave_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(f"Call the Avengers, Music Owner[{member.mention}] has just joined your chat.")
            if member.id in SUDOERS:
                return await message.reply_text(f"Tighten your seatbelts, A member of Music's SudoUser[{member.mention}] has just joined your chat.")
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(f"Welcome To MentosMusic Music\n\nPromote me as administrator in your group otherwise I will not function properly.", reply_markup=InlineKeyboardMarkup(out[1]))
                return
        except:
            return

@Client.on_message(filters.group & filters.command(["start", "help"]))
async def start(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(f"**__Not in allowed chats.__**\n\nMusic Private is only for allowed chats. Ask any Sudo User to allow your chat.\nCheck Sudo Users List [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)")
        return await app.leave_chat(chat_id)
    out = start_pannel()
    await message.reply_text(f"Thanks for having me in {message.chat.title}.\nMusic is alive.\n\nFor any assistance or help, checkout our support group and channel.", reply_markup=InlineKeyboardMarkup(out[1]))
    return
        
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")" 
        await app.send_message(message.chat.id,
            text=f"Hello {rpk}!\n\nThis is ganaMusic Bot.\nI play music on Telegram's Voice Chats.\n\nOnly for selected chats.",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id
        )
    elif len(message.command) == 2:                                                           
        query = message.text.split(None, 1)[1]
        f1 = (query[0])
        f2 = (query[1])
        f3 = (query[2])
        finxx = (f"{f1}{f2}{f3}")
        if str(finxx) == "inf":
            query = ((str(query)).replace("info_","", 1))
            query = (f"https://www.youtube.com/watch?v={query}")
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = (x["thumbnail"])
            searched_text = f"""
π__**Video Track Information**__

βοΈ**Title:** {x["title"]}
   
β³**Duration:** {round(x["duration"] / 60)} Mins
π**Views:** `{x["view_count"]}`
π**Likes:** `{x["like_count"]}`
π**Dislikes:** `{x["dislike_count"]}`
β­οΈ**Average Ratings:** {x["average_rating"]}
π₯**Channel Name:** {x["uploader"]}
π**Channel Link:** [Visit From Here]({x["channel_url"]})
π**Link:** [Link]({x["webpage_url"]})

β‘οΈ __Searched Powered By gana Music Bot__"""
            link = (x["webpage_url"])
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(message.chat.id,
                photo=thumb,                 
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**__Sudo Users List of Music:-__**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:                     
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue                     
                text += f"β€ {user}\n"
            if not text:
                await message.reply_text("No Sudo Users")  
            else:
                await message.reply_text(text)
