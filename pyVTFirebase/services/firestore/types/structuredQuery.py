
import json
import enum

from json import JSONEncoder
from typing import Any, Tuple, Union
from .value import Value


class FieldReference:
    """
    Defines a reference to a document field

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#FieldReference
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

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Projection
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

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#CollectionSelector
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

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Direction
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

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Order
    """

    def __init__(self, field: FieldReference, direction: Direction):
        self._field = field
        self._direction = direction

    def __repr__(self):
        return json.dumps({"field": self._field, "direction": self._direction})

    def data(self):
        return [{"field": self._field, "direction": self._direction}]


class Cursor:
    """
    Defines a position in a query result set

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/Cursor
    """

    def __init__(self, values: Value, before: bool):
        self._values = values
        self._before = before

    def __repr__(self):
        return json.dumps({"values": [self._values], "before": self._before})

    def data(self):
        return {"values": [self._values], "before": self._before}


class FieldFilterOperator(enum.Enum):
    """
    Defines a field filter operator

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Operator_1
    """

    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    ARRAY_CONTAINS = "ARRAY_CONTAINS"
    IN = "IN"
    ARRAY_CONTAINS_ANY = "ARRAY_CONTAINS_ANY"
    NOT_IN = "NOT_IN"

    def data(self):
        if self is self.LESS_THAN:
            return "LESS_THAN"
        elif self is self.LESS_THAN_OR_EQUAL:
            return "LESS_THAN_OR_EQUAL"
        elif self is self.GREATER_THAN:
            return "GREATER_THAN"
        elif self is self.GREATER_THAN_OR_EQUAL:
            return "GREATER_THAN_OR_EQUAL"
        elif self is self.EQUAL:
            return "EQUAL"
        elif self is self.NOT_EQUAL:
            return "NOT_EQUAL"
        elif self is self.ARRAY_CONTAINS:
            return "ARRAY_CONTAINS"
        elif self is self.IN:
            return "IN"
        elif self is self.ARRAY_CONTAINS_ANY:
            return "ARRAY_CONTAINS_ANY"
        elif self is self.NOT_IN:
            return "NOT_IN"


class FieldFilter:
    """
    Defines a filter on a specific document field

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#FieldFilter
    """

    def __init__(self, field: FieldReference, op: FieldFilterOperator, value: Value):
        self.field = field
        self.op = op
        self.value = value

    def __repr__(self):
        return json.dumps({"field": self.field, "op": self.op, "value": self.value})

    def data(self):
        return {"field": self.field, "op": self.op, "value": self.value}


class UnaryFilterOperator(enum.Enum):
    """
    Defines a unary filter operator

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Operator_2
    """

    IS_NAN = "IS_NAN"
    IS_NULL = "IS_NULL"
    IS_NOT_NAN = "IS_NOT_NAN"
    IS_NOT_NULL = "IS_NOT_NULL"

    def data(self):
        if self is self.IS_NAN:
            return "IS_NAN"
        elif self is self.IS_NULL:
            return "IS_NULL"
        elif self is self.IS_NOT_NAN:
            return "IS_NOT_NAN"
        elif self is self.IS_NOT_NULL:
            return "IS_NOT_NULL"


class UnaryFilter:
    """
    Defines a filter with a single operand

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#UnaryFilter
    """

    def __init__(self, field: FieldReference, op: UnaryFilterOperator):
        self.field = field
        self.op = op

    def __repr__(self):
        return json.dumps({"op": self.op, "field": self.field})

    def data(self):
        return {"op": self.op, "field": self.field}


class Filter:
    """
    Defines a filter on a query result set

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Filter
    """

    def __init__(self, filter_type: Union[FieldFilter, UnaryFilter]):
        self.filter_type = filter_type

    def __repr__(self):
        if isinstance(self.filter_type, FieldFilter):
            return json.dumps({"fieldFilter": self.filter_type})
        elif isinstance(self.filter_type, UnaryFilter):
            return json.dumps({"unaryFilter": self.filter_type})

    def data(self):
        if isinstance(self.filter_type, FieldFilter):
            return {"fieldFilter": self.filter_type}
        elif isinstance(self.filter_type, UnaryFilter):
            return {"unaryFilter": self.filter_type}


class StructuredQueryEncoder(JSONEncoder):
    """
    Custom JSON encoder to validate data to serializable JSON
    """

    def default(self, o: Any) -> Any:
        return o.data()
