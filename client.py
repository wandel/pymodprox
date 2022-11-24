import os
import json
import asyncio


class Client:
    async def execute(self, args):
        env = os.environ.copy()
        env['GOPROXY'] = 'direct'
        env['GOPATH'] = 'c:/temp/'
        proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.wait()

        stdout = await proc.stdout.read()
        stderr = await proc.stderr.read()

        if stdout:
            return json.loads(stdout)

        return {'Error': stderr.decode('utf-8')}

    async def get_list(self, package):
        return await self.execute(['go', 'list', '-m', '-versions', '-json', package])

    async def get_latest(self, package):
        return await self.execute(['go', 'list', '-m', '-json', package+'@latest'])

    async def get_info(self, package, version):
        return await self.execute(['go', 'list', '-m', '-json', package+'@'+version])

    async def get_mod(self, package, version):
        return await self.execute(['go', 'list', '-m', '-json', package+'@'+version])

    async def get_archive(self, package, version):
        return await self.execute(['go', 'mod', 'download', '-json', package+'@'+version])


_default = Client()

async def get_list(package):
    return await _default.get_list(package)

async def get_latest(package):
    return await _default.get_latest(package)

async def get_info(package, version):
    return await _default.get_info(package, version)

async def get_mod(package, version):
    return await _default.get_mod(package, version)

async def get_archive(package, version):
    return await _default.get_archive(package, version)