import httpx

from pyVTFirebase.services.helpers import build_url, build_params, validate_json
from pyVTFirebase.exceptions import check_response
from pyVTFirebase.services.auth import Auth
from pyVTFirebase.services.firestore.types.query import Query

from typing import Union


class Firestore:
    """ Firestore Management Service """

    def __init__(self, api_key: str, project_id: str, client: httpx.Client, id_token: str) -> None:
        self.api_key = api_key
        self.project_id = project_id
        self.client = client
        self.id_token = id_token
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents"
        self.header = {"Content-Type": "application/json; charset=UTF-8", "Authorization": f"Bearer {self.id_token}"}

    def refresh_id_token(self, refresh_token: str):
        """
        Refreshes a users auth id token for the auth service when it expires

        :param refresh_token: Firebase Auth refresh token
        """

        auth = Auth(api_key=self.api_key, client=self.client)
        access = auth.exchange_refresh_token_for_ID_token(refresh_token=refresh_token).json()
        self.id_token = access["id_token"]

    def get(self, path: str, mask: list = None) -> httpx.Response:
        """
        Gets the requested document or documents from a collection

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

        url = build_url(self.base_url, path)
        params = build_params(key=self.api_key, mask=mask)

        with self.client as request:
            req = request.get(url=url, headers=self.header, params=params, timeout=3)

        check_response(response=req)
        return req

    def batch_get(self, json_kwargs: dict = None) -> httpx.Response:
        """
        Gets a group of requested documents from the database

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

        url = build_url(self.base_url, delimiter="batchGet")
        params = build_params(key=self.api_key)

        with self.client as request:
            req = request.post(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)

        check_response(response=req)
        return req

    def create(self, collectionId: str, parent: str = None, documentId: str = None,
               mask: list = None, json_kwargs: dict = None) -> httpx.Response:
        """
        Creates a new document in a collection

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

        url = build_url(self.base_url, parent, collectionId)
        params = build_params(key=self.api_key, documentId=documentId, mask=mask)

        with self.client as request:
            req = request.post(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)

        check_response(response=req)
        return req

    def delete(self, path: str, precondition: dict = None) -> httpx.Response:
        """
        Deletes the requested document from a collection

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

        url = build_url(self.base_url, path)
        params = build_params(key=self.api_key, currentDocument=precondition)

        with self.client as request:
            req = request.delete(url=url, headers=self.header, params=params, timeout=3)

        check_response(response=req)
        return req

    def patch(self, path: str, updateMask: list = None, mask: list = None,
              precondition: dict = None, json_kwargs: dict = None) -> httpx.Response:
        """
        Updates or optional creates a document

        :param path: Document path
        :param updateMask: Optional, list of document fields to update. If the document exists on the server and has
                           fields not referenced in the mask, they are left unchanged. Fields referenced in the mask,
                           but not present in the input document, are deleted from the document on the server.
        :param mask: Optional, list of document fields to return from document. If not set, returns all fields.
        :param precondition: Optional, precondition on the document. The request will fail if the precondition isn't
                             met by the target document. Precondition must be None to create a document.
        :param json_kwargs: Structured request parameters for the request body of the request
        :return: Request response form the Firebase REST API

        Examples:
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

        url = build_url(self.base_url, path)
        params = build_params(key=self.api_key, updateMask=updateMask, mask=mask, currentDocument=precondition)

        with self.client as request:
            req = request.patch(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)

        check_response(response=req)
        return req

    def list(self, collectionId: str, parent: str = None, pageSize: int = None, pageToken: str = None,
             orderBy: str = None, mask: list = None, showMissing: bool = False,
             transaction: str = None, readTime: str = None):
        """
        Gets a list of documents from a collection

        :param collectionId: The name of the collection relative to parent to create a document
        :param parent: The parent resource of the collection to get documents from
        :param pageSize: The maximum number of documents to return
        :param pageToken: The nextPageToken value returned from a previous List request, if any
        :param orderBy: The order to sort results by
        :param mask: Optional, list of document fields to return from document. If not set, returns all fields.
        :param showMissing: If the list should show missing documents. A missing document is a document that does not
                            exist bys has sub-documents. These documents will be returned with a key but will not
                            have fields. Request with showMissing may not specify orderBy.
        :param transaction: A base64-encoded transaction string
        :param readTime: Reads documents as they were at the given time. May not be older than 270 seconds.
        :return: Request response form the Firebase REST API

        Examples:
             parent ->
                'Accounts/Company/Employees/...'
            mask ->
                ["Company", "Position"]
           readTime ->
                "2021-07-02T15:01:23Z"

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/list
            https://firebase.google.com/docs/firestore/reference/rest/v1/DocumentMask
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Timestamp
        """

        url = build_url(self.base_url, parent, collectionId)
        params = build_params(key=self.api_key, pageSize=pageSize, pageToken=pageToken, orderBy=orderBy, mask=mask,
                              showMissing=showMissing, transaction=transaction, readTime=readTime)

        with self.client as request:
            req = request.get(url, headers=self.header, params=params, timeout=3)

        check_response(response=req)
        return req

    def runQuery(self, parent: str = None, json_kwargs: Union[dict, Query] = None) -> httpx.Response:
        """
        Runs a custom read query

        :param parent: The parent resource of the collection to run a structured query against
        :param json_kwargs: Structured request parameters for the request body or custom Query object
        :return: Request response form the Firebase REST API

        Examples:
            json_kwargs[dict] ->
                {
                  "structuredQuery": {
                    object (StructuredQuery)
                  },

                  // Union field consistency_selector can be only one of the following:
                  "transaction": string,
                  "newTransaction": {
                    object (TransactionOptions)
                  },
                  "readTime": string
                  // End of list of possible types for union field consistency_selector.
                }

            json_kwargs[Query] ->
                Query object, see query.py in package for details

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/projects.databases.documents/runQuery
            https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery
        """

        json_data = json_kwargs

        if isinstance(json_data, Query):
            json_data = json_data.to_json()

        validate_json(json_data)
        url = build_url(self.base_url, parent, delimiter="runQuery")
        params = build_params(key=self.api_key)

        with self.client as request:
            req = request.post(
                url=url,
                headers=self.header,
                params=params,
                json=json_data,
                timeout=3
            )

        check_response(response=req)
        return req

