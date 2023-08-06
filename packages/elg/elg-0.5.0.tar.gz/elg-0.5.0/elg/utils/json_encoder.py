from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel

try:
    import collections.abc as collections_abc  # python 3.3+
except ImportError:
    import collections as collections_abc

try:
    from dataclasses import asdict, is_dataclass
except ImportError:
    # dataclasses not available
    is_dataclass = lambda x: False
    asdict = lambda x: dict()


def json_provider_class(base, service):
    """
    Create a JSON provider class that calls the `to_json` hook of the given FlaskService/QuartService

    Args:
        base: base class for the returned provider, the DefaultJSONProvider class from either flask or quart
        service: the FlaskService/QuartService instance whose hook should be called
    """

    class ELGJsonProvider(base):
        @staticmethod
        def default(o):
            # First try the service hook
            val = service.to_json(o)
            if val is not None:
                return val
            # Hook did not return a substitute, so fall back on default behaviour
            elif isinstance(o, BaseModel):
                return o.dict(by_alias=True, exclude_none=True)
            elif isinstance(o, collections_abc.Iterable):
                # All iterables will be converted to list.
                return list(o)
            elif isinstance(o, (datetime, date, time)):
                return o.isoformat()
            elif is_dataclass(o):
                return asdict(o)
            elif hasattr(o, "__json__"):
                return o.__json__()
            elif hasattr(o, "for_json"):
                return o.for_json()
            else:
                return base.default(o)

    return ELGJsonProvider
