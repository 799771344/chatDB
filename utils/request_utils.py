import aiohttp

from common.log import logger


async def make_request(method, url, headers, data=None, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method=method, url=url, headers=headers, data=data, **kwargs) as response:
            await logger.debug("request status={}, url={}, data={}".format(response.status, url, data))
            if response.status == 200:
                return await response.content.read()
            else:
                return None


async def make_request_stream(method, url, headers, data=None, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method=method, url=url, headers=headers, data=data, **kwargs) as response:
            await logger.debug("request status={}, url={}, data={}".format(response.status, url, data))
            if response.status == 200:
                async for chunk in response.content.iter_any():
                    yield chunk
            else:
                return
