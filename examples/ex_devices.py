from aioxiq.v2.devices import XiqDevices


async def example():
    api: XiqDevices
    async with XiqDevices() as api:
        return await api.fetch_devices()


async def device_location(dev_id: dict):
    api: XiqDevices
    async with XiqDevices() as api:
        res = await api.get(f"/devices/{dev_id}/location")
        res.raise_for_status()
        body = res.json()
        return body
