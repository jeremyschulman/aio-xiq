from aioxiq import XiqClient


async def example():
    api: XiqClient
    async with XiqClient() as api:
        return await api.paginate("/devices")
