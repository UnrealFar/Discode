from typing import Dict, Any, Optional

class Activity:
    __slots__ = (
        "state",
        "application_id",
        "url",
        "type",
        "name",
    )

    def __init__(self, **kwargs):
        self.state: Optional[str] = kwargs.pop("state", None)
        self.application_id = int(kwargs.pop("application_id", 0))
        self.url = kwargs.pop("url", None)
        self.type = int(kwargs.pop("type", -1))

    def get_payload(self) -> Dict[str, Any]:
        ret = {}
        for attr in self.__slots__:
            item = getattr(self, attr, None)
            if item:
                ret[attr] = item
        
        return ret

