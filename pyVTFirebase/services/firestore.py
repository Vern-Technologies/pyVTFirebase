import httpx

from pyVTFirebase.exceptions import check_response


class Firestore:
    """ Firestore Management Service """

    def __init__(self, api_key, project_id, database_id):
        self.api_key = api_key
        self.project_id = project_id
        self.database_id = database_id
        self.base_url = 'https://firestore.googleapis.com'
        self.header = {"Content-Type": "application/json; charset=UTF-8"}

    def documents_get(self):
        pass
