import json

from pyVTFirebase.services.firestore.types import FieldReference, Projection, CollectionSelector, Order, \
    Direction, StructuredQueryEncoder
from typing import Iterable, Tuple


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
                if value == "_from_coll":
                    data["structuredQuery"]["from"] = vars(self)[value]
                if value == "_orderBy":
                    data["structuredQuery"]["orderBy"] = vars(self)[value]
                if value == "_offset":
                    data["structuredQuery"]["offset"] = vars(self)[value]
                if value == "_limit":
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

    def fromCollection(self, collection: Tuple) -> "Query":
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
            raise ValueError(f"Size of Tuple is expected to be 2 elements, not {len(collection)}")

        for i, coll in enumerate(collection):
            if i == 0:
                if not isinstance(coll, str):
                    raise TypeError(f"Index 0 of Tuple collection isn't of type String")
            if i == 1:
                if not isinstance(coll, bool):
                    raise TypeError(f"Index 1 of Tuple collection isn't of type Bool")

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

    def order_by(self, field: str, direction: str = "ASCENDING") -> "Query":
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

    def offset(self, offset: int) -> "Query":
        """
        Offsets the results to return from the start. Applies after all other constraints. Must be greater
        than 0 if specified.

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
