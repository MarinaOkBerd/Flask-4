import sys
import asyncio
import aiohttp
import requests
import threading
from time import perf_counter
from multiprocessing import Process

urls = [
    'https://cdn-front.kwork.ru/pics/t3/51/4295605-1579887251.jpg',
    'https://top-fon.com/uploads/posts/2023-01/1674702822_top-fon-com-p-fon-dlya-prezentatsii-programmista-117.jpg'
    'https://office-guru.ru/wp-content/uploads/2021/06/904f2a80-07af-11ea-8ce9-3d2153bbfe0d.png',
]


def download_sync(url):
    start_time = perf_counter()
    response = requests.get(url)
    filename = url.split('/')[-1]
    filename = 'downloads/' + filename
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Загружен {url} за {perf_counter() - start_time:.2f}")


async def download_async(url: str):
    start_time = perf_counter()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.content.read()
            filename = url.split('/')[-1]
            filename = 'downloads/' + filename
            with open(filename, "wb", ) as f:
                f.write(img)
    print(f"Загружен {url} за {perf_counter() - start_time:.2f}")


def download_threading(urls):
    threads = []
    start_time = perf_counter()

    for url in urls:
        thread = threading.Thread(target=download_sync, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Загружены за {perf_counter() - start_time:.2f}")


def download_process(urls):
    processes = []
    start_time = perf_counter()

    for url in urls:
        thread = Process(target=download_sync, args=(url,))
        processes.append(thread)
        thread.start()

    for process in processes:
        process.join()

    print(f"Загружены за {perf_counter() - start_time:.2f}")


async def download_asyncio(urls):
    start_time = perf_counter()
    await asyncio.gather(*[await asyncio.to_thread(download_async, url) for url in urls])
    print(f"Загружены за {perf_counter() - start_time:.2f}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        urls = sys.argv[1:]

    download_threading(urls)
    download_process(urls)
    asyncio.run(download_asyncio(urls))
