from .services import Auth, Firestore


def setup(config):
    return Connection(config)


class Connection:

    def __init__(self, config):
        self.api_key = config["apiKey"]

    def auth(self):
        return Auth(self.api_key)

    def firestore(self):
        return Firestore(self.api_key)


