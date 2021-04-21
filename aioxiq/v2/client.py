from typing import Optional
import os
from httpx import AsyncClient


class XiqBaseClient(AsyncClient):
    DEFAULT_URL = "https://api.extremecloudiq.com"
    DEFAULT_TIMEOUT = 10

    def __init__(
        self,
        *vargs,
        xiq_user: Optional[str] = None,
        xiq_password: Optional[str] = None,
        xiq_token: Optional[str] = None,
        **kwargs,
    ):
        kwargs.setdefault("base_url", self.DEFAULT_URL)
        kwargs.setdefault("timeout", self.DEFAULT_TIMEOUT)
        super(XiqBaseClient, self).__init__(*vargs, **kwargs)

        self.xiq_user = xiq_user or os.getenv("XIQ_USER")
        self.xiq_password = xiq_password or os.getenv("XIQ_PASSWORD")
        self.xiq_token = xiq_token or os.getenv("XIQ_TOKEN")
        if self.xiq_token:
            self.headers["Authorization"] = "Bearer " + self.xiq_token

    async def login(
        self, username: Optional[str] = None, password: Optional[str] = None
    ):
        creds = {
            "username": username or self.xiq_user,
            "password": password or self.xiq_password,
        }
        res = await self.post("/login", json=creds)
        res.raise_for_status()
        self.xiq_token = res.json()["access_token"]
        self.headers["Authorization"] = "Bearer " + self.xiq_token
