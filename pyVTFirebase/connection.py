from .services import Auth, Firestore


def setup(config: dict):
    return Connection(config)


class Connection:

    def __init__(self, config: dict):
        self.api_key = config["apiKey"]
        self.project_id = config["projectID"]

    def auth(self):
        return Auth(api_key=self.api_key)

    def firestore(self, idToken: str):
        return Firestore(api_key=self.api_key, project_id=self.project_id, id_token=idToken)



