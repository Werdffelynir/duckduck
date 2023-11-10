#!/bin/python3

import sys
import aiohttp
import asyncio
from aiohttp import ClientConnectorError

out: dict = {'decided': 0, 'errors': 0, 'messages': {}, }


async def fetch(url, session):
    try:
        async with session.get(url) as response:
            out['decided'] += 1
            return await response.text()
    except ClientConnectorError:
        out['errors'] += 1
        out['messages'][url] = 'ClientConnectorError'
    except:
        out['errors'] += 1
        out['messages'].append((url, 'Error'))


async def main():
    file_path = 'data.list'

    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in urls]
        await asyncio.gather(*tasks)
        print('Common: {}; Decided: {}; Errors: {} \n{}'.format(
            out['decided'] + out['errors'],
            out['decided'],
            out['errors'],
            "".join([f'{err}: {out["messages"][err]}\n' for err in out['messages']]),
        ))


if __name__ == "__main__":
    loop: int = sys.argv[1] if len(sys.argv) - 1 else 1
    print('DDuck fly ' + str(loop) + ' mm')
    while loop:
        asyncio.run(main())
        loop -= 1
