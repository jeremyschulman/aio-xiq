from typing import Optional

from .client import XiqBaseClient


class XiqLocations(XiqBaseClient):
    def __init__(self, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self._locations_tree = dict()
        self._locations_parents = dict()
        self._locations_names = dict()

    async def build_locations_tree(self):
        """
        This coroutine is used to fetch the entire locations tree data
        structure and form the relationships between the parent and child
        locations.  This coroutine must be called before using the
        device_locations_tree coroutine.
        """
        tree = await self._fetch_locations_tree()
        self._walk_children(parent_id=0, dot=tree[0])

    async def device_locations_tree(
        self, device_id: Optional[int] = None, device: Optional[dict] = None
    ):
        """
        This coroutine is used to return the list of locations for the given
        device.  The list of locations is a list of tuples, where each tuple is
        the (location_id, location_name).  The first item in the list is the
        location of the device.  The last item in the list is the root of the
        location tree.

        Parameters
        ----------
        device_id: int
            When provided, this coroutine will use the value to fetch
            the device location record.

        device: dict
            The device location record

        Returns
        -------
        List[Tuple[int, str]] as described.
        """
        if device_id:
            res = await self.get(f"/devices/{device_id}/location")
            res.raise_for_status()
            device = res.json()

        return [x async for x in self._device_tree(device)]

    # -------------------------------------------------------------------------
    #
    #                           PRIVATE METHODS
    #
    # -------------------------------------------------------------------------

    async def _fetch_locations_tree(self):
        res = await self.get("/locations/tree")
        res.raise_for_status()
        self._locations_tree = res.json()
        return self._locations_tree

    def _walk_children(self, parent_id: int, dot: dict):
        my_id = dot["id"]
        my_name = dot["name"]

        self._locations_parents[my_id] = parent_id
        self._locations_names[my_id] = my_name

        my_childs = dot["children"]
        for ch in my_childs:
            self._walk_children(parent_id=my_id, dot=ch)

    async def _device_tree(self, device: dict):
        """
        This generator yeilds each location-tree leaf starting
        with the parent location of the device `parent_id`.  Each
        yielded value is a Tuple(parent_id, parent_name)

        Parameters
        ----------
        device: dict
            The device record from the /devices/{id}/location API.

        Yields
        -------
        Tuple[int, str] as described.
        """

        # Pull the first child of the device parent, which would be the
        # location of the device.  For some reason the device record
        # location_id value is match matched in the output of the
        # /locations/tree API.
        # TODO: open question with Extreme.

        parent_id = device["parent_id"]
        res = await self.get("/locations/tree", params=dict(parentId=parent_id))
        res.raise_for_status()
        first_loc = res.json()[0]
        yield device["location_id"], first_loc["name"]

        while parent_id != 0:
            loc_name = self._locations_names[parent_id]
            yield parent_id, loc_name
            parent_id = self._locations_parents[parent_id]
