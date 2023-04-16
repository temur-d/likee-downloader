from random import randint
from os import path

from aiohttp import ClientSession
from aiofiles import ospath, os, open

async def download_video(url: str) -> str:

    if not await ospath.exists('downloaded_videos'):
        await os.mkdir('downloaded_videos')

    file_name = randint(1000000000, 1000000000000)
    file_directory = f'downloaded_videos\\{file_name}.mp4'
    file_directory = path.abspath(file_directory)

    async with ClientSession() as session:

        async with session.get(url=url) as get_request:
            video_content = await get_request.content.read()

            async with open(file=file_directory, mode='wb') as file:
                await file.write(video_content)

    return file_directory
            