
import json
import datetime


def build_url(*args, delimiter: str = None) -> str:

    url = ""

    for _i, _sub in enumerate(args):
        if _sub is not None:
            if isinstance(_sub, str):
                if _i != len(args) - 1:
                    url += _sub + "/"
                else:
                    url += _sub
            else:
                raise ValueError("Argument is not of type string")

    if delimiter:
        url += delimiter

    return url


def build_params(**kwargs) -> dict:

    params = {}

    for key in kwargs:
        if kwargs.get(key) is not None:
            ident = key

            if ident == "mask":
                ident = "mask.fieldPaths"

            params[ident] = kwargs.get(key)

    return params


def validate_json(json_text: dict):
    if isinstance(input, dict):
        try:
            return json.loads(str(json_text))
        except Exception as e:
            raise ValueError(f"Invalid json: {e}")


def build_body(**kwargs) -> dict:

    data = {}

    for _key in kwargs:
        if _key == "mask":
            if isinstance(kwargs.get(_key), list):
                data[_key] = {
                    "fieldPaths": kwargs.get(_key)
                }
        elif _key == "documents":
            if isinstance(kwargs.get(_key), list):
                data[_key] = kwargs.get(_key)
        elif _key == "readTime":
            if isinstance(kwargs.get(_key), int):
                if 0 <= kwargs.get(_key) <= 269:
                    data[_key] = _currentTime(minus=kwargs.get(_key))
                else:
                    raise ValueError("readTime not within limits of 0 <= readTime <= 269")

    return data


def _currentTime(minus: int = None) -> str:

    time = datetime.datetime.now(datetime.timezone.utc)

    if minus:
        time -= datetime.timedelta(seconds=minus)

    time.isoformat()

    return time.strftime('%Y-%m-%dT%H:%M:%SZ')
