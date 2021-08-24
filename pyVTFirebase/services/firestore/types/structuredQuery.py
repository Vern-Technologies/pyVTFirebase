import json
import enum

from json import JSONEncoder
from typing import Any, Tuple


class FieldReference:
    """
    Defines a reference to a document field
    """

    def __init__(self, field_path: str = None):
        self._field_path = field_path

    def __repr__(self):
        return json.dumps({"fieldPath": self._field_path})

    def data(self):
        return {"fieldPath": self._field_path}


class Projection:
    """
    Defines a project of document fields to return
    """

    def __init__(self, fields: list = None):
        self._fields = fields

    def __repr__(self):
        return json.dumps(({"fields": self._fields}))

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields: list):
        for field in fields:
            if not isinstance(field, FieldReference):
                raise ValueError("List element not of type StructuredQuery.FieldReference")

    def data(self):
        return {"fields": self._fields}


class CollectionSelector:
    """
    Defines a selection of a collection
    """

    def __init__(self, collections: Tuple = None):
        self._collections = collections

    def __repr__(self):
        return json.dumps([{"collectionId": self._collections[0], "allDescendants": self._collections[1]}])

    def data(self):
        return [{"collectionId": self._collections[0], "allDescendants": self._collections[1]}]


class Direction(enum.Enum):
    """
    Defines a sort direction
    """

    DIRECTION_UNSPECIFIED = "DIRECTION_UNSPECIFIED"
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"

    def data(self):
        if self is self.ASCENDING:
            return "ASCENDING"
        elif self is self.DESCENDING:
            return "DESCENDING"
        elif self is self.DIRECTION_UNSPECIFIED:
            return "DIRECTION_UNSPECIFIED"


class Order:
    """
    Defines an order on a field
    """

    def __init__(self, field: FieldReference, direction: Direction):
        self._field = field
        self._direction = direction

    def __repr__(self):
        return json.dumps({"field": self._field, "direction": self._direction})

    def data(self):
        return [{"field": self._field, "direction": self._direction}]


class StructuredQueryEncoder(JSONEncoder):
    """
    Custom JSON encoder to validate data to serializable JSON
    """

    def default(self, o: Any) -> Any:
        return o.data()

