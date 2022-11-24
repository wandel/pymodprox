import logging
import argparse

import aiohttp.web
import aiohttp.abc

lookup = {
    'http://gopkg.in/check.v1': 'gopkg.in/check.v1 git https://github.com/go-check/check.git',
}


@aiohttp.web.middleware
async def handler(request: aiohttp.web.Request, handler):
    if 'go-get' not in request.query:
        logging.warning('message="non go-get request received"')
        raise aiohttp.web.HTTPNotFound

    if request.path not in lookup:
        logging.warning('message="not mapped"')
        raise aiohttp.web.HTTPNotFound

    mapping = lookup[request.path]
    logging.info('host="%s", path="%s", mapping="%s"', request.host, request.path, mapping)
    entry = f'<meta name="go-import" content="{mapping}" />'
    return aiohttp.web.Response(text=f'<html><head>'+entry+'</head></html>', content_type="text/html")


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
