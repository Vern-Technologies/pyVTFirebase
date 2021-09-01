
import json
import math

from .structuredQuery import FieldReference, Projection, CollectionSelector, Order, Direction, Cursor, FieldFilter, \
    FieldFilterOperator, UnaryFilter, UnaryFilterOperator, Filter, StructuredQueryEncoder
from .value import Value

from typing import Iterable, Tuple, Union, Any


_EQ_OP: str
_operator_enum: Any
_BAD_OP_STRING: str
_BAD_OP_NAN_NULL: str
_KEY: str

_EQ_OP = "=="
_operator_enum = FieldFilterOperator
_COMPARISON_OPERATORS = {
    "<": _operator_enum.LESS_THAN,
    "<=": _operator_enum.LESS_THAN_OR_EQUAL,
    ">": _operator_enum.GREATER_THAN,
    ">=": _operator_enum.GREATER_THAN_OR_EQUAL,
    _EQ_OP: _operator_enum.EQUAL,
    "!=": _operator_enum.NOT_EQUAL,
    "array_contains": _operator_enum.ARRAY_CONTAINS,
    "in": _operator_enum.IN,
    "array_contains_any": _operator_enum.ARRAY_CONTAINS_ANY,
    "not_in": _operator_enum.NOT_IN
}
_BAD_OP_STRING = "Operator string {!r} is invalid. Valid choices are: {}."
_BAD_OP_NAN_NULL = 'Only an equality filter ("==") can be used with None or NaN values'


class Query(object):

    def __init__(
            self,
            select=None,
            from_coll=None,
            where=None,
            orderBy=None,
            startAt=None,
            endAt=None,
            offset=None,
            limit=None
    ) -> None:
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
                self._select == other._select
                and self._from_coll == other._from_coll
                and self._where == other._where
                and self._orderBy == other._orderBy
                and self._startAt == other._startAt
                and self._endAt == other._endAt
                and self._offset == other._offset
                and self._limit == other._limit
        )

    def to_json(self):
        """
        Converts the Query class parameters to serializable JSON for passing into httpx request to
        the Firebase REST API

        :return:
        """

        data = {"structuredQuery": {}}

        for value in vars(self):
            if vars(self)[value]:
                if value == "_select":
                    data["structuredQuery"]["select"] = vars(self)[value]
                elif value == "_from_coll":
                    data["structuredQuery"]["from"] = vars(self)[value]
                elif value == "_where":
                    data["structuredQuery"]["where"] = vars(self)[value]
                elif value == "_orderBy":
                    data["structuredQuery"]["orderBy"] = vars(self)[value]
                elif value == "_startAt":
                    data["structuredQuery"]["startAt"] = vars(self)[value]
                elif value == "_endAt":
                    data["structuredQuery"]["endAt"] = vars(self)[value]
                elif value == "_offset":
                    data["structuredQuery"]["offset"] = vars(self)[value]
                elif value == "_limit":
                    data["structuredQuery"]["limit"] = vars(self)[value]

        return json.loads(json.dumps(data, cls=StructuredQueryEncoder))

    def select(self, field_paths: Iterable[str]) -> "Query":
        """
        Creates a projection of document fields to return

        :param field_paths: List of document field names to return
        :return: New instance of the Query class

        Examples:
            field_Paths: ["Name", "Description"]

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Projection
        """

        field_paths = list(field_paths)

        "Type verification"
        for field in field_paths:
            if not isinstance(field, str):
                raise TypeError("Field path of field_paths isn't of type str")

        new_select = Projection(
            fields=[
                FieldReference(field_path=field_path) for field_path in field_paths
            ]
        )

        return self.__class__(
            select=new_select.data(),
            from_coll=self._from_coll,
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit

        )

    def fromCollection(self, collection: Tuple[str, bool]) -> "Query":
        """
        Creates a selection of a collection to query from

        :param collection: Tuple of collection to query from
        :return: New instance of the Query class

        Examples:
            collection: ("Customers", False)
            collection[0]:
                collectionId: Selects only collections with this ID
            collection[1]:
                allDescendants: When false, selects only collections that are immediate children of the parent
                                specified in the containing Query. When True, selects all descendant collections.

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#CollectionSelector
        """

        # Type and size verification
        if len(collection) != 2:
            raise ValueError(f"Size of collection Tuple is expected to be 2 elements, not {len(collection)}")

        if not isinstance(collection[0], str):
            raise TypeError(f"Index 0 of collection Tuple has to be of type str not {type(collection[0])}")
        if not isinstance(collection[1], bool):
            raise TypeError(f"Index 1 of collection Tuple has to be of type bool not {type(collection[1])}")

        new_from_coll = CollectionSelector(collections=collection)

        return self.__class__(
            select=self._select,
            from_coll=new_from_coll.data(),
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit
        )

    def where(
            self,
            field: str,
            op: str,
            key: str = None,
            value: Union[None, bool, str, bytes, int, float, Tuple[float, float], dict] = None) -> "Query":
        """

        :param field:
        :param op:
        :param key:
        :param value:
        :return:
        """

        # Type verification
        if not isinstance(field, str):
            raise TypeError(f"Field is required to be of type str not {type(field)}")
        if not isinstance(op, str):
            raise TypeError(f"Op is required to be of type str not {type(op)}")
        if key:
            if not isinstance(key, str):
                raise TypeError(f"Key is required to be of type str not {type(key)}")

        if value is None:
            if op != _EQ_OP:
                raise ValueError(_BAD_OP_NAN_NULL)
            where = Filter(UnaryFilter(field=FieldReference(field_path=field), op=UnaryFilterOperator.IS_NULL))
        elif _isnan(value):
            if op != _EQ_OP:
                raise ValueError(_BAD_OP_NAN_NULL)
            where = Filter(UnaryFilter(field=FieldReference(field_path=field), op=UnaryFilterOperator.IS_NAN))
        else:
            where = Filter(FieldFilter(field=FieldReference(field_path=field), op=_field_filter_op_string(op=op),
                                       value=Value(key=key, value=value)))

        return self.__class__(
            select=self._select,
            from_coll=self._from_coll,
            where=where.data(),
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit
        )

    def orderBy(self, field: str, direction: str = "ASCENDING") -> "Query":
        """
        Creates a order on a field.

        Multiple calls of this function will add order conditions to the Query object.

        :param field: The field of documents to order by
        :param direction: The direction to order by. Defaults to ASCENDING.
        :return: New instance of the Query class

        Examples:
            field: "Amount"
            direction: ("ASCENDING", "DESCENDING", "DIRECTION_UNSPECIFIED")

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Order
            https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery#Direction
        """

        # Type verification
        if not isinstance(field, str):
            raise TypeError("Field isn't of type str")

        # Set direction
        if direction == "ASCENDING":
            direction = Direction.ASCENDING
        elif direction == "DESCENDING":
            direction = Direction.DESCENDING
        elif direction == "DIRECTION_UNSPECIFIED":
            direction = Direction.DIRECTION_UNSPECIFIED
        else:
            raise ValueError(f"Direction specification not possible for {type(direction)}: {direction}")

        new_order = Order(field=FieldReference(field_path=field), direction=direction)
        order = self._orderBy + new_order.data() if self._orderBy is not None else new_order.data()

        return self.__class__(
            select=self._select,
            from_coll=self._from_coll,
            where=self._where,
            orderBy=order,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit
        )

    def startAt(self, key: str, value: Union[None, bool, str, int, float, Tuple[float, float], dict] = None,
                before: bool = True) -> "Query":
        """
        Creates a cursor object that represents a starting position for the query results

        :param key: The type of value object to generate
        :param value: The value of the value object to generate. Represents a position in the order they appear in the
                      order by clause of a query.
        :param before: If the position is just before or just after the given value, relative to the sort order
                       defined by the query.
        :return: New instance of the Query class

        Example:
            key options:
                'null': Creates a nullValue object. Value parameter isn't required.
                'bool': Creates a booleanValue object.
                'int': Creates a integerValue object.
                'double': Creates a doubleValue object.
                'time': Creates a timestampValue object.
                'string': Creates a stringValue object.
                'bytes': Creates a bytesValue object.
                'ref': Creates a referenceValue object.
                'geo': Creates a geoPointValue object.
                'array': Creates a arrayValue object.
                'map': Creates a mapValue object.


            key: "int"          key: "geo"
            value: 23           value: (64.8942944, -52.1294764)
            before: True        before: True

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/Cursor
            https://firebase.google.com/docs/firestore/reference/rest/v1/Value
        """

        # Type verification
        if not isinstance(key, str):
            raise TypeError(f"key must be of type str not {type(key)}")
        if not isinstance(before, bool):
            raise TypeError(f"before must be of type bool not {type(before)}")

        new_start = Cursor(before=before, values=Value(key=key, value=value))

        return self.__class__(
            select=self._select,
            from_coll=self._from_coll,
            where=self._where,
            orderBy=self._orderBy,
            startAt=new_start.data(),
            endAt=self._endAt,
            offset=self._offset,
            limit=self._limit
        )

    def endAt(self, key: str, value: Union[None, bool, str, int, float, Tuple[float, float], dict] = None,
              before: bool = True) -> "Query":
        """
        Creates a cursor object that represents a ending position for the query results

        :param key: The type of value object to generate
        :param value: The value of the value object to generate. Represents a position in the order they appear in the
                      order by clause of a query.
        :param before: If the position is just before or just after the given value, relative to the sort order
                       defined by the query.
        :return: New instance of the Query class

        Example:
            key options:
                'null': Creates a nullValue object. Value parameter isn't required.
                'bool': Creates a booleanValue object.
                'int': Creates a integerValue object.
                'double': Creates a doubleValue object.
                'time': Creates a timestampValue object.
                'string': Creates a stringValue object.
                'bytes': Creates a bytesValue object.
                'ref': Creates a referenceValue object.
                'geo': Creates a geoPointValue object.
                'array': Creates a arrayValue object.
                'map': Creates a mapValue object.


            key: "int"          key: "geo"
            value: 23           value: (64.8942944, -52.1294764)
            before: True        before: True

        Links: ->
            https://firebase.google.com/docs/firestore/reference/rest/v1/Cursor
            https://firebase.google.com/docs/firestore/reference/rest/v1/Value
        """

        # Type verification
        if not isinstance(key, str):
            raise TypeError(f"key must be of type str not {type(key)}")
        if not isinstance(before, bool):
            raise TypeError(f"before must be of type bool not {type(before)}")

        new_end = Cursor(before=before, values=Value(key=key, value=value))

        return self.__class__(
            select=self._select,
            from_coll=self._from_coll,
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=new_end.data(),
            offset=self._offset,
            limit=self._limit
        )

    def offset(self, offset: int) -> "Query":
        """
        Offsets the results to return from the start. Applies before limit but after all other constraints. Must be
        greater than 0 if specified.

        :param offset: The number of results to skip
        :return: New instance of the Query class
        """

        # Type verification
        if isinstance(offset, bool):
            raise TypeError("Offset isn't of type int")
        if not isinstance(offset, int):
            raise TypeError("Offset isn't of type int")

        return self.__class__(
            select=self._select,
            from_coll=self._from_coll,
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=offset,
            limit=self._limit
        )

    def limit(self, limit: int) -> "Query":
        """
        Limits the number of results to return. Applies after all other constraints. Must be greater
        than 0 if specified.

        :param limit: The maximum number of results to return
        :return: New instance of the Query class
        """

        # Type verification
        if isinstance(limit, bool):
            raise TypeError("Offset isn't of type int")
        if not isinstance(limit, int):
            raise TypeError("Limit isn't of type int")

        return self.__class__(
            select=self._select,
            from_coll=self._from_coll,
            where=self._where,
            orderBy=self._orderBy,
            startAt=self._startAt,
            endAt=self._endAt,
            offset=self._offset,
            limit=limit
        )


def _isnan(value) -> bool:
    """
    Check if a value is NaN

    This differs from ``math.isnan`` in that **any** input type is allowed

    :param value: A value to check for NaN-ness.
    :return: Indicates if the value is the NaN float
    """
    if isinstance(value, float):
        return math.isnan(value)
    else:
        return False


def _field_filter_op_string(op: str) -> _operator_enum:
    """
    Convert a string representation of a FieldFilterOperator to an enum

    :param op: A comparison operation in the form of a string
            Acceptable values are (
                '<', '<=', '>', '>=', '==', '!=', 'array_contains', 'in', 'array_contains_any', 'not_in'
            )
    :return: The enum corresponding to the string representation of a FieldFilterOperator
    """
    try:
        return _COMPARISON_OPERATORS[op]
    except KeyError:
        choices = ", ".join(sorted(_COMPARISON_OPERATORS.keys()))
        msg = _BAD_OP_STRING.format(op, choices)
        raise ValueError(msg)
