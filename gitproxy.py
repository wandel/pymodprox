import logging
import argparse

import aiohttp.web


@aiohttp.web.middleware
async def handler(request: aiohttp.web.Request, handler):
    response = aiohttp.web.StreamResponse()
    async with aiohttp.ClientSession() as client:
        async with client.get("https://github.com"+request.path) as resp:
            response.set_status(resp.status)
            await response.prepare(request)
            async for chunk, _ in resp.content.iter_chunks():
                await response.write(chunk)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='127.0.0.1', help='the address to listen on')
    parser.add_argument('-p', '--port', default=3000, help='the port to listen on')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    app = aiohttp.web.Application(middlewares=[handler])
    aiohttp.web.run_app(app, host=args.address, port=args.port)


if __name__ == '__main__':
    main()
