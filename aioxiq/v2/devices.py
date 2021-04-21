from typing import Optional

from .client import XiqBaseClient


class XiqDevices(XiqBaseClient):
    """
    APIs as defined:
    https://api.extremecloudiq.com/swagger-ui/index.html?configUrl=/openapi/swagger-config#/Device
    """

    async def fetch_devices(self, page: Optional[int] = 1, limit: Optional[int] = 50):
        await self.get("/")
