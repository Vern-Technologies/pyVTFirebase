import httpx

from pyVTFirebase.exceptions import check_response


class Firestore:
    """ Firestore Management Service """

    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = 'https://firestore.googleapis.com/v1/'
        self.header = {"Content-Type": "application/json; charset=UTF-8", "Authorization": None}

    def get(self, idToken: str, path: str, fields: list = None) -> httpx.Response:
        """
        Gets the requested document or documents from a collection

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param path: Document or Collection path
        :param fields: List of document fields to request from document
        :return: Request response form the Firebase REST API

        Path Example:
            "Credentials/Team/<UserID>"
        Fields Example:
            ["Company", "Role", "Name"]
        """

        # Set to empty list if no fields are supplied. Httpx doesn't omits params whose values are None
        if fields is None:
            fields = []

        url = self.base_url + f"projects/{self.project_id}/databases/(default)/documents/{path}"
        self.header["Authorization"] = f"Bearer {idToken}"
        params = {"key": self.api_key, "mask.fieldPaths": fields}
        req = httpx.get(url=url, headers=self.header, params=params, timeout=3)
        check_response(response=req)
        return req

    def document_batch_get(self, idToken: str, documents: list = None, fields: list = None) -> httpx.Response:
        """
        Gets the requested documents from the database

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param documents: List of document path to request
        :param fields: List of document fields to request from document
        :return: Request response form the Firebase REST API

        Documents Example:
            ["Credentials/Team/<UserID>", "Credentials/Team/<UserID>", "Accounts/Company/<ResourceID>"]
        Fields Example:
            ["Company", "Role"]
        """

        projectPath = f"projects/{self.project_id}/databases/(default)/documents"
        data = {}

        if documents:
            data["documents"] = [(projectPath + f"/{path}") for path in documents]
        if fields:
            data["mask"] = {
                "fieldPaths": fields
            }

        url = self.base_url + projectPath + ':batchGet'
        self.header["Authorization"] = f"Bearer {idToken}"
        params = {"key": self.api_key}
        req = httpx.post(url=url, headers=self.header, params=params, json=data, timeout=3)
        check_response(response=req)
        return req

    def update(self, idToken: str):
        pass
