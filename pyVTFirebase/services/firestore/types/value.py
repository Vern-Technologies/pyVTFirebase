
import json
import datetime

from typing import Union, Tuple


class Value:
    """
    Defines a message to be used within a cursor

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/Value
    """

    def __init__(self, key: str, value: Union[None, bool, str, int, float, Tuple[float, float], dict] = None):

        def determine() -> Union[NullValue, BooleanValue, IntegerValue, DoubleValue, TimestampValue, StringValue,
                                 BytesValue, ReferenceValue, GeoPointValue, ArrayValue, MapValue]:

            if not isinstance(key, str):
                raise TypeError(f"Key must be of type str not {type(key)}")

            if key == "null":
                if value is None:
                    return NullValue()
                else:
                    raise TypeError(f"Key null requires parameter value to be None not {type(value)}")
            elif key == "bool":
                if isinstance(value, bool):
                    return BooleanValue(boolean=value)
                else:
                    raise TypeError(f"Key bool requires parameter value to be of type bool not {type(value)}")
            elif key == "int":
                if isinstance(value, int):
                    return IntegerValue(integer=value)
                else:
                    raise TypeError(f"Key int requires parameter value to be of type int not {type(value)}")
            elif key == "double":
                if isinstance(value, float):
                    return DoubleValue(double=value)
                else:
                    raise TypeError(f"Key double requires parameter value to be of type float not {type(value)}")
            elif key == "time":
                if isinstance(value, (str, int)):
                    return TimestampValue(timestamp=value)
                else:
                    raise TypeError(f"Key time requires parameter value to be of type str or int not {type(value)}")
            elif key == "string":
                if isinstance(value, str):
                    return StringValue(string=value)
                else:
                    raise TypeError(f"Key string requires parameter value to be of type str not {type(value)}")
            elif key == "bytes":
                if isinstance(value, str):
                    return BytesValue(bytesValue=value)
                else:
                    raise TypeError(f"Key bytes requires parameter value to be of type str not {type(value)}")
            elif key == "ref":
                if isinstance(value, str):
                    return ReferenceValue(reference=value)
                else:
                    raise TypeError(f"Key ref requires parameter value to be of type str not {type(value)}")
            elif key == "geo":
                if isinstance(value, Tuple):
                    return GeoPointValue(geo=value)
                else:
                    raise TypeError(f"Key geo requires parameter value to be of type tuple not {type(value)}")
            elif key == "array":
                if isinstance(value, dict):

                    def raiseError():
                        raise KeyError(
                            "Value for key array can only contain 2 elements with the key names 'key' and 'value'")

                    if len(value.keys()) != 2:
                        raiseError()

                    for keys in value.keys():
                        if keys not in ["key", "value"]:
                            raiseError()

                    return ArrayValue(value=Value(key=value["key"], value=value["value"]))
                else:
                    raise TypeError(f"Key array requires parameter value to be of type dict not {type(value)}")
            elif key == "map":
                if isinstance(value, dict):

                    def raiseError():
                        raise KeyError(
                            "Value for key map can only contain 2 elements with the key names 'key' and 'value'")

                    def check(checking: dict):
                        if len(checking.keys()) != 2:
                            raiseError()

                        for key_checking in checking.keys():
                            if key_checking not in ["key", "value"]:
                                raiseError()

                    check(checking=value)
                    check(checking=value["value"])

                    return MapValue(key=value["key"], value=Value(
                        key=value["value"]["key"], value=value["value"]["value"]))
                else:
                    raise TypeError(f"Key map requires parameter value to be of type dict not {type(value)}")
            else:
                raise ValueError(f"Key {key} doesn't correspond to a known type. Must either be"
                                 "[null, bool, int, double, time, string, bytes, ref, geo, array, map]")

        self._value_type = determine().data()

    def __repr__(self):
        return json.dumps(self._value_type)

    def data(self):
        return self._value_type


class NullValue:
    """
    Defines a NullValue object of a message
    """

    def __init__(self):
        self._null = "NULL_VALUE"

    def __repr__(self):
        return json.dumps({"nullValue": self._null})

    def data(self):
        return {"nullValue": self._null}


class BooleanValue:
    """
    Defines a BooleanValue object of a message
    """

    def __init__(self, boolean: bool):
        self._boolean = boolean

    def __repr__(self):
        return json.dumps({"booleanValue": self._boolean})

    def data(self):
        return {"booleanValue": self._boolean}


class IntegerValue:
    """
    Defines a IntegerValue object of a message
    """

    def __init__(self, integer: int):
        self._integer = integer

    def __repr__(self):
        return json.dumps({"integerValue": self._integer})

    def data(self):
        return {"integerValue": self._integer}


class DoubleValue:
    """
    Defines a DoubleValue object of a message
    """

    def __init__(self, double: float):
        self._double = double

    def __repr__(self):
        return json.dumps({"doubleValue": self._double})

    def data(self):
        return {"doubleValue": self._double}


class TimestampValue:
    """
    Defines a TimestampValue object of a message

    Pass in your own "Zulu" formatted datetime string or an offset value to have the class define its own. Offset value
    must be within 0 <= "Offset" <= 269.
    """

    def __init__(self, timestamp: Union[int, str]):

        def currentTime(minus: int = None) -> str:
            time = datetime.datetime.now(datetime.timezone.utc)

            if minus:
                if 0 <= minus <= 269:
                    time -= datetime.timedelta(seconds=minus)
                else:
                    raise ValueError(f"Time calculation value supplied: {minus} not within limits 0 <= value <= 269")

            time.isoformat()
            return time.strftime('%Y-%m-%dT%H:%M:%SZ')

        self._time = currentTime(minus=timestamp) if isinstance(timestamp, int) else timestamp

    def __repr__(self):
        return json.dumps({"timestampValue": self._time})

    def data(self):
        return {"timestampValue": self._time}


class StringValue:
    """
    Defines a StringValue object of a message
    """

    def __init__(self, string: str):
        self._string = string

    def __repr__(self):
        return json.dumps({"stringValue": self._string})

    def data(self):
        return {"stringValue": self._string}


class BytesValue:
    """
    Defines a BytesValue object of a message
    """

    def __init__(self, bytesValue: str):
        self._bytesValue = bytesValue

    def __repr__(self):
        return json.dumps({"bytesValue": self._bytesValue})

    def data(self):
        return {"bytesValue": self._bytesValue}


class ReferenceValue:
    """
    Defines a ReferenceValue object of a message
    """

    def __init__(self, reference: str):
        self._reference = reference

    def __repr__(self):
        return json.dumps({"referenceValue": self._reference})

    def data(self):
        return {"referenceValue": self._reference}


class GeoPointValue:
    """
    Defines a GeoPointValue object of a message

    An object that represents a latitude/longitude pair. This is expressed as a pair of floats to represent degrees
    latitude and degrees longitude. This must conform to the WGS84 standard. Values must be within normalized ranges.

    WGS84 Standards: https://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/Shared.Types/LatLng
    """

    def __init__(self, geo: Tuple[float, float]):
        """
        Initializes the LatLng class

        :param geo: Tuple of coordinates
            geo[0] - latitude: The latitude in degrees. Must be in the range [-90.0, +90.0].
            geo[1] - longitude: The longitude in degrees. Must be in the range [-180.0, +180.0]
        """

        def raiseError():
            raise ValueError("Value for key geo can only contain 2 elements of type float corresponding to Geo "
                             "coordinates latitude and longitude")

        # Check geo
        if len(geo) != 2:
            raiseError()

        for index in range(0, 2):
            if not isinstance(geo[index], float):
                raiseError()

        self._latitude = geo[0]
        self._longitude = geo[1]

    def __repr__(self):
        return json.dumps({"geoPointValue": {"latitude": self._latitude, "longitude": self._longitude}})

    def data(self):
        return {"geoPointValue": {"latitude": self._latitude, "longitude": self._longitude}}


class ArrayValue:
    """
    Defines a ArrayValue object of a message

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/ArrayValue
    """

    def __init__(self, value: Value):
        self._value = value

    def __repr__(self):
        return json.dumps({"arrayValue": {"values": [self._value.data()]}})

    def data(self):
        return {"arrayValue": {"values": [self._value.data()]}}


class MapValue:
    """
    Defines a MapValue object of a message

    Links: ->
        https://firebase.google.com/docs/firestore/reference/rest/v1/Value#MapValue
    """

    def __init__(self, key: str, value: Value):
        self._key = key
        self._value = value

    def __repr__(self):
        return json.dumps({"mapValue": {"fields": {self._key: self._value.data()}}})

    def data(self):
        return {"mapValue": {"fields": {self._key: self._value.data()}}}
