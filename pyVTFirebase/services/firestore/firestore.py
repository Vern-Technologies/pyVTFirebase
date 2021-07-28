import httpx

from .helpers import build_url, build_params, validate_json
from pyVTFirebase.exceptions import check_response


class Firestore:
    """ Firestore Management Service """

    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.project_path = f"projects/{self.project_id}/databases/(default)/documents"
        self.base_url = "https://firestore.googleapis.com/v1"
        self.header = {"Content-Type": "application/json; charset=UTF-8", "Authorization": None}

    def get(self, idToken: str, path: str, mask: list = None) -> httpx.Response:
        """
        Gets the requested document or documents from a collection

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param path: Document or Collection path
        :param mask: List of document fields to request from document
        :return: Request response form the Firebase REST API

        Examples:
            path ->
                "Credentials/Team/<UserID>"
            mask ->
                ["Company", "Role", "Name"]

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/get
        """

        url = build_url(self.base_url, self.project_path, path)
        self.header["Authorization"] = f"Bearer {idToken}"
        params = build_params(key=self.api_key, mask=mask)
        req = httpx.get(url=url, headers=self.header, params=params, timeout=3)
        check_response(response=req)
        return req

    def batch_get(self, idToken: str, json_kwargs: dict = None) -> httpx.Response:
        """
        Gets a group of requested documents from the database

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param json_kwargs: Structured request parameters for the request body of the request
        :return: Request response form the Firebase REST API

        Example:
            json_kwargs ->
                {
                    "documents": [
                        string
                    ],
                    "mask": {
                        object (DocumentMask)
                    },

                    // Union field can be only one of the following:
                    "transaction": string,
                    "newTransaction": {
                        object (TransactionOptions)
                    },
                    "readTime": string
                    // End of list of possible types for union field.
                }

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/batchGet
        """

        validate_json(json_kwargs)

        url = build_url(self.base_url, self.project_path, delimiter=":batchGet")
        self.header["Authorization"] = f"Bearer {idToken}"
        params = build_params(key=self.api_key)
        req = httpx.post(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)
        check_response(response=req)
        return req

    def create(self, idToken: str, collectionId: str, parent: str = None, documentId: str = None,
               mask: list = None, json_kwargs: dict = None) -> httpx.Response:
        """
        Creates a new document in a collection

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param collectionId: The name of the collection relative to parent to create a document
        :param parent: The parent resource of the collection to create a document
        :param documentId: Optional, self assigned document ID. If not specified, an ID will be assigned by Firebase.
        :param mask: Optional, list of document fields to return from document creation. If not set, returns all fields.
        :param json_kwargs: Structured request parameters for the request body of the request
        :return: Request response form the Firebase REST API

        Examples:
            The request body contains an instance of a document

            parent ->
                'Accounts/Company/Employees/...'
            mask ->
                ["Company", "Role", "Name"]
            json_kwargs ->
                // Document instance
                {
                    "name": string,
                    "fields": {
                        string: {
                            object (Value)
                        },
                        ...
                    },
                    "createTime": string,
                    "updateTime": string
                }

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/createDocument
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents#Document
            https://firebase.google.com/docs/firestore/reference/rest/v1/Value
        """

        validate_json(json_kwargs)

        url = build_url(self.base_url, self.project_path, parent, collectionId)
        self.header["Authorization"] = f"Bearer {idToken}"
        params = build_params(key=self.api_key, documentId=documentId, mask=mask)
        req = httpx.post(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)
        check_response(response=req)
        return req

    def delete(self, idToken: str, path: str, precondition: dict = None) -> httpx.Response:
        """
        Deletes the requested document from a collection

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param path: Document path
        :param precondition: Optional, precondition on the document. The request will fail if the precondition isn't
                             met by the target document.
        :return: Request response form the Firebase REST API

        Example:
            path ->
                'Accounts/Company/Employees/...'
            precondition ->
                // Precondition instance
                {
                  // Union field can be only one of the following:
                  "exists": boolean,
                  "updateTime": string
                  // End of list of possible types for union field.
                }

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/delete
            https://firebase.google.com/docs/firestore/reference/rest/v1/Precondition
        """

        validate_json(precondition)

        url = build_url(self.base_url, self.project_path, path)
        self.header["Authorization"] = f"Bearer {idToken}"
        params = build_params(key=self.api_key, currentDocument=precondition)
        req = httpx.delete(url=url, headers=self.header, params=params, timeout=3)
        check_response(response=req)
        return req

    def patch(self, idToken: str, path: str, updateMask: list = None, mask: list = None,
              precondition: dict = None, json_kwargs: dict = None) -> httpx.Response:
        """
        Updates or optional creates a document

        :param idToken: The Firebase Auth ID token for the application user making the request
        :param path: Document path
        :param updateMask: Optional, list of document fields to update. If the document exists on the server and has
                           fields not referenced in the mask, they are left unchanged. Fields referenced in the mask,
                           but not present in the input document, are deleted from the document on the server.
        :param mask: Optional, list of document fields to return from document. If not set, returns all fields.
        :param precondition: Optional, precondition on the document. The request will fail if the precondition isn't
                             met by the target document. Precondition must be None to create a document.
        :param json_kwargs: Structured request parameters for the request body of the request
        :return: Request response form the Firebase REST API

        Example:
            path ->
                'Accounts/Company/Employees/...'
            updateMask ->
                ["Company", "Role", "Name"]
            mask ->
                ["Company", "Position"]
            precondition ->
                // Precondition instance
                {
                  // Union field can be only one of the following:
                  "exists": boolean,
                  "updateTime": string
                  // End of list of possible types for union field.
                }
            json_kwargs ->
                // Document instance
                {
                    "name": string,
                    "fields": {
                        string: {
                            object (Value)
                        },
                        ...
                    },
                    "createTime": string,
                    "updateTime": string
                }

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/patch
            https://firebase.google.com/docs/firestore/reference/rest/v1/DocumentMask
            https://firebase.google.com/docs/firestore/reference/rest/v1/Precondition
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents#Document
        """

        validate_json(precondition, json_kwargs)

        url = build_url(self.base_url, self.project_path, path)
        self.header["Authorization"] = f"Bearer {idToken}"
        params = build_params(key=self.api_key, updateMask=updateMask, mask=mask, currentDocument=precondition)
        req = httpx.patch(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)
        check_response(response=req)
        return req

