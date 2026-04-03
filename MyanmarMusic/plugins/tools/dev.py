
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MyanmarMusic import app
from config import OWNER_ID


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_edited_message(
    filters.command("eval")
    & filters.user([OWNER_ID])
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("eval")
    & filters.user([OWNER_ID])
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ ?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if stdout:
        evaluation += stdout
    if stderr:
        evaluation += stderr
    if exc:
        evaluation += exc
    t2 = time()
    eval_time = "{:.3f}".format(t2 - t1)
    final_output = f"<b>OUTPUT</b>\n\n<code>{evaluation.strip()}</code>\n\n<b>Time:</b> <code>{eval_time}s</code>"
    if len(final_output) > 4096:
        with open("output.txt", "w") as f:
            f.write(evaluation.strip())
        await message.reply_document("output.txt")
    else:
        await edit_or_reply(message, text=final_output, parse_mode="html")


@app.on_callback_query(filters.regex("close_eval"))
async def close_eval(client, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_edited_message(
    filters.command("sh")
    & filters.user([OWNER_ID])
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("sh")
    & filters.user([OWNER_ID])
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                stdout, stderr = process.communicate()
                result = str(stdout.decode().strip()) + str(stderr.decode().strip())
                output += f"<code>{result}</code>\n"
            except Exception as e:
                output += f"<code>{e}</code>\n"
        return await edit_or_reply(message, text=output, parse_mode="html")
    shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
    try:
        process = subprocess.Popen(
            shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    except Exception as e:
        result = str(e)
    await edit_or_reply(message, text=f"<code>{result}</code>", parse_mode="html")
