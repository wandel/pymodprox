import argparse
import logging

import aiohttp.web

import client


def unescape(package: str):
    result = ''
    bang = False
    for rune in package:
        if bang:
            result += rune.upper()
            bang = False
        elif rune == '!':
            bang = True
        else:
            result += rune
    return result


async def list_handler(request: aiohttp.web.Request):
    package = unescape(request.match_info['package'])
    result = await client.get_list(package)
    if 'Error' in result:
        return aiohttp.web.Response(text=result['Error'], status=404)

    return aiohttp.web.Response(text='\n'.join(result['Versions']))


async def latest_handler(request: aiohttp.web.Request):
    package = unescape(request.match_info['package'])
    result = await client.get_latest(package)
    if 'Error' in result:
        return aiohttp.web.Response(text=result['Error'], status=404)

    return aiohttp.web.json_response({
        'Time': result['Time'],
        'Version': result['Version'],
    })


async def info_handler(request: aiohttp.web.Request):
    package = unescape(request.match_info['package'])
    version = request.match_info['version']
    result = await client.get_info(package, version)
    if 'Error' in result:
        return aiohttp.web.Response(text=result['Error'], status=404)

    return aiohttp.web.json_response({
        'Time': result['Time'],
        'Version': result['Version'],
    })


async def mod_handler(request: aiohttp.web.Request):
    package = unescape(request.match_info['package'])
    version = request.match_info['version']
    result = await client.get_mod(package, version)
    if 'Error' in result:
        return aiohttp.web.Response(text=result['Error'], status=404)

    with open(result['GoMod'], 'rb') as f:
        return aiohttp.web.Response(body=f.read(), content_type='text/plain', charset='UTF-8')


async def zip_handler(request: aiohttp.web.Request):
    package = unescape(request.match_info['package'])
    version = request.match_info['version']
    result = await client.get_archive(package, version)
    if 'Error' in result:
        return aiohttp.web.Response(text=result['Error'], status=404)

    return aiohttp.web.FileResponse(result['Zip'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='127.0.0.1', help='the address to listen on')
    parser.add_argument('-p', '--port', default=3000, help='the port to listen on')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    app = aiohttp.web.Application()

    app.add_routes([
        aiohttp.web.get(r'/{package:.+}/@v/list', list_handler),
        aiohttp.web.get(r'/{package:.+}/@latest', latest_handler),
        aiohttp.web.get(r'/{package:.+}/@v/{version:.+}.info', info_handler),
        aiohttp.web.get(r'/{package:.+}/@v/{version:.+}.mod', mod_handler),
        aiohttp.web.get(r'/{package:.+}/@v/{version:.+}.zip', zip_handler),
    ])
    aiohttp.web.run_app(app, host=args.address, port=args.port)


if __name__ == '__main__':
    main()