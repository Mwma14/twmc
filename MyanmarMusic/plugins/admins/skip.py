from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode  # <-- ParseMode ထည့်ထားသည်

import config
from MyanmarMusic import YouTube, app
from MyanmarMusic.core.call import Hotty
from MyanmarMusic.misc import db
from MyanmarMusic.utils.database import get_loop
from MyanmarMusic.utils.decorators import AdminRightsCheck
from MyanmarMusic.utils.inline import close_markup, stream_markup
from MyanmarMusic.utils.stream.autoclear import auto_clean
from MyanmarMusic.utils.thumbnails import get_thumb
from config import BANNED_USERS

def get_stream_text(t, d, u):
    t = str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    u = str(u).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    return (
        f"<blockquote><emoji id='5895705279416241926'>🎧</emoji> <b>စတင်ထုတ်လွှင့်နေပြီ</b> |</blockquote>\n"
        f"<blockquote><emoji id='6120465303177533732'>🎵</emoji> <b>ခေါင်းစဉ် :</b> {t[:27]}\n"
        f"<emoji id='6120591326107935086'>⏱</emoji> <b>ကြာချိန် :</b> {d} ᴍɪɴᴜᴛᴇs\n"
        f"<emoji id='6120398056874582504'>👤</emoji> <b>တောင်းဆိုသူ :</b> {u}</blockquote>"
    )


@app.on_message(
    filters.command(["skip", "cskip", "next", "cnext"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    if not len(message.command) < 2:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(_["admin_8"])
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = int(count - 1)
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except:
                                return await message.reply_text(_["admin_12"])
                            if popped:
                                await auto_clean(popped)
                            if not check:
                                try:
                                    await message.reply_text(
                                        text=_["admin_6"].format(
                                            message.from_user.mention,
                                            message.chat.title,
                                        ),
                                        reply_markup=close_markup(_),
                                    )
                                    await Hotty.stop_stream(chat_id)
                                except:
                                    return
                                break
                    else:
                        return await message.reply_text(_["admin_11"].format(count))
                else:
                    return await message.reply_text(_["admin_10"])
            else:
                return await message.reply_text(_["queue_2"])
        else:
            return await message.reply_text(_["admin_9"])
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await message.reply_text(
                    text=_["admin_6"].format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(_),
                )
                try:
                    return await Hotty.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await message.reply_text(
                    text=_["admin_6"].format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(_),
                )
                return await Hotty.stop_stream(chat_id)
            except:
                return
    queued = check[0]["file"]
    title = (check[0]["title"]).title()
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    videoid = check[0]["vidid"]
    status = True if str(streamtype) == "video" else None
    db[chat_id][0]["played"] = 0
    exis = (check[0]).get("old_dur")
    if exis:
        db[chat_id][0]["dur"] = exis
        db[chat_id][0]["seconds"] = check[0]["old_second"]
        db[chat_id][0]["speed_path"] = None
        db[chat_id][0]["speed"] = 1.0
        
    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            return await message.reply_text(_["admin_7"].format(title))
        try:
            image = await YouTube.thumbnail(videoid, True)
        except:
            image = None
        try:
            await Hotty.skip_stream(chat_id, link, video=status, image=image)
        except:
            return await message.reply_text(_["call_6"])
        button = stream_markup(_, chat_id)
        img = await get_thumb(videoid)
        
        # 🟢 get_stream_text အသုံးပြုခြင်း
        run = await message.reply_photo(
            photo=img,
            caption=get_stream_text(title, check[0]["dur"], user),
            reply_markup=InlineKeyboardMarkup(button),
            parse_mode=ParseMode.HTML,
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
        
    elif "vid_" in queued:
        mystic = await message.reply_text(_["call_7"], disable_web_page_preview=True)
        try:
            file_path, direct = await YouTube.download(
                videoid,
                mystic,
                videoid=True,
                video=status,
            )
        except:
            return await mystic.edit_text(_["call_6"])
        try:
            image = await YouTube.thumbnail(videoid, True)
        except:
            image = None
        try:
            await Hotty.skip_stream(chat_id, file_path, video=status, image=image)
        except:
            return await mystic.edit_text(_["call_6"])
        button = stream_markup(_, chat_id)
        img = await get_thumb(videoid)
        
        # 🟢 get_stream_text အသုံးပြုခြင်း
        run = await message.reply_photo(
            photo=img,
            caption=get_stream_text(title, check[0]["dur"], user),
            reply_markup=InlineKeyboardMarkup(button),
            parse_mode=ParseMode.HTML,
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await mystic.delete()
        
    elif "index_" in queued:
        try:
            await Hotty.skip_stream(chat_id, videoid, video=status)
        except:
            return await message.reply_text(_["call_6"])
        button = stream_markup(_, chat_id)
        
        index_text = (
            f"<blockquote><emoji id='5895705279416241926'>🎧</emoji> <b>စတင်ထုတ်လွှင့်နေပြီ (Index Stream)</b> |</blockquote>\n"
            f"<blockquote><emoji id='6120591326107935086'>👤</emoji> <b>တောင်းဆိုသူ :</b> {user}</blockquote>"
        )
        
        run = await message.reply_photo(
            photo=config.STREAM_IMG_URL,
            caption=index_text,
            reply_markup=InlineKeyboardMarkup(button),
            parse_mode=ParseMode.HTML,
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
        
    else:
        if videoid == "telegram":
            image = None
        elif videoid == "soundcloud":
            image = None
        else:
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
        try:
            await Hotty.skip_stream(chat_id, queued, video=status, image=image)
        except:
            return await message.reply_text(_["call_6"])
            
        if videoid == "telegram":
            button = stream_markup(_, chat_id)
            
            # 🟢 get_stream_text အသုံးပြုခြင်း
            run = await message.reply_photo(
                photo=config.TELEGRAM_AUDIO_URL
                if str(streamtype) == "audio"
                else config.TELEGRAM_VIDEO_URL,
                caption=get_stream_text(title, check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
                parse_mode=ParseMode.HTML,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            
        elif videoid == "soundcloud":
            button = stream_markup(_, chat_id)
            
            # 🟢 get_stream_text အသုံးပြုခြင်း
            run = await message.reply_photo(
                photo=config.SOUNCLOUD_IMG_URL
                if str(streamtype) == "audio"
                else config.TELEGRAM_VIDEO_URL,
                caption=get_stream_text(title, check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
                parse_mode=ParseMode.HTML,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            
        else:
            button = stream_markup(_, chat_id)
            img = await get_thumb(videoid)
            
            # 🟢 get_stream_text အသုံးပြုခြင်း
            run = await message.reply_photo(
                photo=img,
                caption=get_stream_text(title, check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
                parse_mode=ParseMode.HTML,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
