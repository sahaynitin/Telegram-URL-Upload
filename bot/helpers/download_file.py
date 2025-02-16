import os
import asyncio
from pyrogram.types import Message


async def run_command(*args, messages: Message):
    process = await asyncio.create_subprocess_exec(
        *args,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE)
    await messages.edit_text('Downloading Start..')
    # print("Started:", args, "(pid = " + str(process.pid) + ")", flush=True)
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        await messages.edit_text('Downloading complected')
        # print("Done:", command, "(pid = " + str(process.pid) + ")", flush=True)
    else:
        await messages.edit_text('Downloading Failed')
        # print(
        #     "Failed:", command, "(pid = " + str(process.pid) + ")", flush=True
        # )
    # Return stdout
    value = None
    for i in stdout.decode().split('\n'):
        if i.startswith('[download] Destination:'):
            value = i.replace('[download] Destination:', '').strip(' ')

    if value is None:
        return value

    return value


async def download_file(url: str, download_location: str, messages: Message) -> str:
    commands = [
        "youtube-dl",
        "--no-warnings",
        '-o',
        download_location,
        url,
    ]

    # output = subprocess.check_output(commands)
    output = await run_command(*commands, messages=messages)
    # error = e.output.decode().strip()
    # raise ErrorLinkToFile(f'{error}')
    if output is None:
        return False
    f = os.path.abspath(output)
    if os.path.isfile(f) is not True:
        return False

    return f

# loop = asyncio.get_event_loop()
# r = loop.run_until_complete(download_file('https://de20.seedr.cc/ff_get/1061871730/WWW.YIFY-TORRENTS.COM.jpg?st=cLRD77ytKvSgskFsHG5QqA&e=1638858214'))
# print(r)
