
from .types import StructuredQuery
from typing import Any, Dict, Generator, Iterable, NoReturn, Optional, Tuple, Union


class Query(object):

    def __init__(
            self,
            parent,
            select=None,
            from_coll=None,
            where=None,
            orderBy=None,
            startAt=None,
            endAt=None,
            offset=None,
            limit=None
    ) -> None:
        self._parent = parent
        self._select = select
        self._from_coll = from_coll
        self._where = where
        self._orderBy = orderBy
        self._startAt = startAt
        self._endAt = endAt
        self._offset = offset
        self._limit = limit

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._parent == other._parent
            and self._select == other._select
            and self._from_coll == other._from_coll
            and self._where == other._where
            and self._orderBy == other._orderBy
            and self._startAt == other._startAt
            and self._endAt == other._endAt
            and self._offset == other._offset
            and self._limit == other._limit
        )

    def _to_json(self):

        data = {}

        for value in vars(self):

            if vars(self)[value]:

                if value == "_select":

                    data["select"] = vars(self)[value]

                if value == "_from_coll":

                    data["from"] = vars(self)[value]

        return data

    def select(self, field_paths: Iterable[str]) -> "Query":
        """

        :param field_paths:
        :return:
        """

        field_paths = list(field_paths)

        new_select = StructuredQuery.Projection(
            fields=[
                StructuredQuery.FieldReference(field_path=field_path) for field_path in field_paths
            ]
        )

        return self.__class__(
            parent=self._parent,
            select=new_select.data(),
            from_coll=self._from_coll,
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit

        )

    def fromCollection(self, collections: Iterable[Tuple]) -> "Query":
        """

        :param collections:
        :return:
        """

        collections = list(collections)

        # Type verification
        for i, coll in enumerate(collections):
            if isinstance(coll, Tuple):
                if not isinstance(coll[0], str):
                    raise TypeError(f"Index 0 of Iterable Tuple at index {i} isn't of type String")
                if not isinstance(coll[1], bool):
                    raise TypeError(f"Index 1 of Iterable Tuple at index {i} isn't of type Bool")
            else:
                raise TypeError("Iterable in collections isn't of type Tuple")

        new_from_coll = StructuredQuery.CollectionSelector(collections=collections)

        return self.__class__(
            parent=self._parent,
            select=self._select,
            from_coll=new_from_coll.data(),
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit
        )
