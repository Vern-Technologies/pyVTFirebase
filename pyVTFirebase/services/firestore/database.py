
import httpx

from typing import Any, Dict, Generator, Iterable, NoReturn, Optional, Tuple, Union
from pyVTFirebase.services.helpers import build_url, build_params
from pyVTFirebase.exceptions import check_response
from .query import Query


class Database(object):

    def __init__(self, parent: str, api_key: str, project_id: str, client: httpx.Client, id_token: str):
        self.api_key = api_key
        self.project_id = project_id
        self.client = client
        self.id_token = id_token
        self.parent = parent
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents"
        self.header = {"Content-Type": "application/json; charset=UTF-8", "Authorization": f"Bearer {self.id_token}"}

    def _query(self) -> Query:
        return Query(self)

    def select(self, field_paths: Iterable[str]) -> Query:

        query = self._query()
        return query.select(field_paths=field_paths)

    def fromCollection(self, collections: Iterable[Tuple]) -> Query:

        query = self._query()
        return query.fromCollection(collections=collections)

    def get(self):

        print(self._to_json())

        # url = build_url(self.base_url, self.parent, delimiter="runQuery")
        # params = build_params(key=self.api_key)
        #
        # with self.client as request:
        #     req = request.post(url=url, headers=self.header, params=params, json=json_kwargs, timeout=3)
        #
        # check_response(response=req)
        # return req

