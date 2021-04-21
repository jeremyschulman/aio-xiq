from aioxiq.v2 import XiqBaseClient, XiqAuth


class Client(XiqAuth, XiqBaseClient):
    pass


api = Client()
