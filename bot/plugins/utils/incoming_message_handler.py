import time
from bot.linktofile import TG
from pyrogram import filters
from pyrogram.types import Message, InputMediaPhoto
from bot import REGEX, DOWNLOAD_LOCATION
from bot.helpers import link_check, download_file, file_send, remove_file


@TG.on_message(filters.regex(pattern='.*http.*'))
async def incoming_urls(client: TG, message: Message) -> None:
    url = message.text
    if '|' in url:
        url, file_name = url.replace(' ', '').split('|')
        download_location = DOWNLOAD_LOCATION.format(message.from_user.id, int(time.time()), file_name)
    else:
        download_location = DOWNLOAD_LOCATION.format(message.from_user.id, int(time.time()), '%(title)s.%(ext)s')

    url_check = await link_check(url, message)
    if url_check is False:
        await message.reply(f'The link is not valid or something is wrong with the bot. Contact **[Abhijith N T]('
                            f'tg://user?id=429320566)** or create a new issue with GitHub.')
        return
    _reply = await client.send_message(
        message.chat.id,
        f'**URL:** {url} is valid',
        reply_to_message_id=message.message_id
    )

    file_download_path = await download_file(url, download_location, _reply)
    await _reply.delete()
    if file_download_path is False:
        await message.reply('Sorry file path is not found')
        return
    try:
        await file_send(file_download_path, client, message)
        remove_file(file_download_path)
    except Exception as err:
        await client.send_message(
            message.chat.id,
            f'File uploading error',
            reply_to_message_id=message.message_id
        )


