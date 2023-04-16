import asyncio
from fake_useragent import UserAgent
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from download import download_video

BASE_URL = 'https://www.expertstool.com'

async def download_url(url: str) -> str:

    user_agent = UserAgent().random
    headers = {'user-agent': user_agent}

    async with ClientSession() as session:
        
        try:
            async with session.get(url=f'{BASE_URL}/like-video-download', headers=headers) as get_request:
                if get_request.ok:
                    
                    html = await get_request.text(encoding='utf-8')
                    soup = BeautifulSoup(html, 'lxml')
                    
                    post_request_url = soup.find('form', method='post').get('action')
                    key_url = soup.find('form', method='post').find('input').get('name')
                    
                    data = {key_url: url}

            async with session.post(url=f'{BASE_URL}{post_request_url}', data=data, headers=headers) as post_request:
                if post_request.ok:

                    html = await post_request.text(encoding='utf-8')
                    soup = BeautifulSoup(html, 'lxml')

                    video_url = soup.find('video').get('src')
                    video_url = video_url.replace('\/', '/').removesuffix('","')
                    
                    return video_url
        except Exception:
            return None

    
async def main() -> None:
    
    url = input('Paste video link from TikTok: ')
    print('Please wait...')
    url = await download_url(url=url)

    if url is not None:
        print('Downloading video...')
        file_directory = await download_video(url=url)
        print(f'Video downloaded.\nFull path: {file_directory}')
    else:
        print('Unable to download video, something went wrong...')

if __name__ == '__main__':
    asyncio.run(main())
