import json
from aioxiq import XiqClient
from aioxiq.v2.locations import XiqLocations

api = XiqLocations()
tree_data = json.load(open("../location-tree.json"))

locations = dict()
location_names = dict()


def walk_children(parent_id: int, dot: dict):
    my_id = dot["id"]
    my_name = dot["name"]

    locations[my_id] = parent_id
    location_names[my_id] = my_name

    # G.add_node(my_id, name=my_name)
    # G.add_edge(my_id, parent_id)

    print("id:{id}, name:{name}".format(id=my_id, name=my_name))
    my_childs = dot["children"]
    for ch in my_childs:
        walk_children(parent_id=my_id, dot=ch)


async def location_tree(device: dict):
    parent_id = device["parent_id"]
    res = await api.get("/locations/tree", params=dict(parentId=parent_id))
    res.raise_for_status()
    first_loc = res.json()[0]
    yield device["location_id"], first_loc["name"]

    while parent_id != 0:
        loc_name = location_names[parent_id]
        yield parent_id, loc_name
        parent_id = locations[parent_id]
