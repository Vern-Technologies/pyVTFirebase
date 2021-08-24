
import json

from json import JSONEncoder
from typing import Any, Tuple


class StructuredQuery:
    """A Firestore query.

        select (google.cloud.firestore_v1.types.StructuredQuery.Projection):
            The projection to return.
        from_ (Sequence[google.cloud.firestore_v1.types.StructuredQuery.CollectionSelector]):
            The collections to query.
        where (google.cloud.firestore_v1.types.StructuredQuery.Filter):
            The filter to apply.
        order_by (Sequence[google.cloud.firestore_v1.types.StructuredQuery.Order]):
            The order to apply to the query results.

            Firestore guarantees a stable ordering through the following
            rules:

            -  Any field required to appear in ``order_by``, that is not
               already specified in ``order_by``, is appended to the
               order in field name order by default.
            -  If an order on ``__name__`` is not specified, it is
               appended by default.

            Fields are appended with the same sort direction as the last
            order specified, or 'ASCENDING' if no order was specified.
            For example:

            -  ``SELECT * FROM Foo ORDER BY A`` becomes
               ``SELECT * FROM Foo ORDER BY A, __name__``
            -  ``SELECT * FROM Foo ORDER BY A DESC`` becomes
               ``SELECT * FROM Foo ORDER BY A DESC, __name__ DESC``
            -  ``SELECT * FROM Foo WHERE A > 1`` becomes
               ``SELECT * FROM Foo WHERE A > 1 ORDER BY A, __name__``
        start_at (google.cloud.firestore_v1.types.Cursor):
            A starting point for the query results.
        end_at (google.cloud.firestore_v1.types.Cursor):
            A end point for the query results.
        offset (int):
            The number of results to skip.
            Applies before limit, but after all other
            constraints. Must be >= 0 if specified.
        limit (google.protobuf.wrappers_pb2.Int32Value):
            The maximum number of results to return.
            Applies after all other constraints.
            Must be >= 0 if specified.
    """

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
                if not isinstance(field, StructuredQuery.FieldReference):
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

    class StructuredQueryEncoder(JSONEncoder):
        """
        Custom JSON encoder to validate data to serializable JSON
        """

        def default(self, o: Any) -> Any:
            return o.data()
