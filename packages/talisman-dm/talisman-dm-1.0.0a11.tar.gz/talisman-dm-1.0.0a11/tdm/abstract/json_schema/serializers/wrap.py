from typing import Any, Dict, List, Mapping, Set

from .abstract import AbstractElementSerializer

_COLLECTIONS: Mapping[type, type] = {
    tuple: List,  # in other case Tuple[A, ...] is converted to Tuple[A]. Deserializes to tuple
    set: Set,
    list: List
}


class WrappedElementSerializer(AbstractElementSerializer):
    def __init__(self, real_type: type, serializer: AbstractElementSerializer):
        self._real_type = real_type
        self._typing_type = _COLLECTIONS[real_type]
        self._serializer = serializer

    def serialize(self, element):
        return self._real_type(self._serializer.serialize(e) for e in element)

    def deserialize(self, serialized, typed_id2element: Dict[type, Dict[str, Any]]):
        return self._real_type(self._serializer.deserialize(s, typed_id2element) for s in serialized)

    def field_type(self, element_type):
        return self._typing_type[self._serializer.field_type(element_type)]
