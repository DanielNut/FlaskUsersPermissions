from datetime import datetime
from pprint import pprint
import asyncio
import aiohttp
import async_timeout
import click
from itertools import chain

urls = [
    'http://127.0.0.1:5000/array1',
    'http://127.0.0.1:5000/array2',
    'http://127.0.0.1:5000/array3'
]


async def fetch_args(session, url):
    try:
        async with async_timeout.timeout(2):
            async with session.get(url) as response:
                data = await response.json(content_type='text/html')
                return data
    except:
        return []


async def main():
    async with aiohttp.ClientSession() as session:
        # create a collection of coroutines(can be done with comprehension )
        fetch_coroutines = []
        for url in urls:
            fetch_coroutines.append(fetch_args(session, url))
        # waik up coroutines with gather
        data = await asyncio.gather(*fetch_coroutines)
        # create plain iterable from data
        data = chain(*data)
        data = sorted(data, key=lambda x: int(x['id']))
        pprint(data)


start = datetime.now()
asyncio.run(main())
click.secho(f"{datetime.now() - start}", bold=True, bg="blue", fg="white")
