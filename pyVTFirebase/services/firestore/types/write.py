import enum
import datetime

from typing import Union


class DocumentMask(object):

    def __init__(self, fields: list):
        """

        :param fields: List of field paths.
        """

        self.fieldPaths = fields

    def __repr__(self):
        return {
            "fieldPaths": self.fieldPaths
        }


class ServerValue(enum.Enum):
    SERVER_VALUE_UNSPECIFIED = "SERVER_VALUE_UNSPECIFIED"
    REQUEST_TIME = "REQUEST_TIME"


class Timestamp:

    def __init__(self):

        def currentTime() -> str:
            time = datetime.datetime.now(datetime.timezone.utc)
            time.isoformat()

            return time.strftime('%Y-%m-%dT%H:%M:%SZ')

        self.time = currentTime()


class LatLng:
    """
    An object that represents a latitude/longitude pair. This is expressed as a pair of doubles to represent degrees
    latitude and degrees longitude. Unless specified otherwise, this must conform to the WGS84 standard. Values must
    be within normalized ranges.

    WGS84 Standards: https://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf
    """

    def __init__(self, latitude: float, longitude: float):
        """
        Initializes the LatLng class

        :param latitude: The latitude in degrees. Must be in the range [-90.0, +90.0].
        :param longitude: The longitude in degrees. Must be in the range [-180.0, +180.0]
        """

        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class Value:

    def __init__(self, value: Union[None, bool, str, float, Timestamp, bytes, LatLng, ArrayValue, MapValue]):
        self.value_type = value


class MapValue:

    def __init__(self, key: str, value: Value):
        self.key = key
        self.value = value

    def __repr__(self):
        return {
            "fields": {
                self.key: {
                    self.value
                }
            }
        }


class ArrayValue:

    def __init__(self, values: Value):
        self.values = values

    def __repr__(self):
        return {
            "values": [
                {
                    self.values
                }
            ]
        }


class FieldTransform(object):
    """ A transformation of a field of the document """

    def __init__(self, field: str):
        """

        :param field: The document field
        """

        self.fieldPath = field
        self.transform_type: Union[ServerValue, Value, ArrayValue]


class Precondition:
    """ A precondition on a document, used for conditional operations """

    def __init__(self, condition: Union[bool, str]):
        """

        :param condition: conditional check to execute operation

            options: exists -> bool : When set to TRUE, the target document must exist. When set to False, the target
                                      document must not exist.
                     updateTime -> String (Timestamp format) : When set, the target document must exist and have been
                                                               last updated at that time.
        """

        self.condition_type = condition

    def __repr__(self):
        if type(self.condition_type) is bool:
            return {
                "exists": self.condition_type
            }
        else:
            return {
                "updateTime": self.condition_type
            }


class DocumentTransform(object):
    """ A transformation of a document """

    def __init__(self, document: str, fieldTransforms: FieldTransform):
        self.document = document
        self.fieldTransforms = fieldTransforms

    def __repr__(self):
        return {
            "document": self.document,
            "fieldTransforms": [
                {
                    self.fieldTransforms
                }
            ]
        }


class Write(object):

    def __init__(self, fields: DocumentMask = None, transforms: FieldTransform = None, precondition: Precondition = None):
        self.updateMask = fields
        self.updateTransforms = transforms
        self.currentDocument = precondition
        # self.operation: Union[Document, str, DocumentTransform]
        self.update = None
        self.delete = ""
        self.transform = None

    def __repr__(self):
        writes = {
            "writes": [
                {

                }
            ]
        }
