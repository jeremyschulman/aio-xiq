from aioxiq.v2 import XiqAuth


class Client(XiqAuth):
    pass


async def test():
    async with Client() as api:
        await api.login()
        print(await api.fetch_permissions())
        print(await api.fetch_token_info())
