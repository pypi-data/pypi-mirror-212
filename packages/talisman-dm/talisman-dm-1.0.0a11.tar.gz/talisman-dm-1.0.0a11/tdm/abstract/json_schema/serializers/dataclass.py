from typing import Any, Type

from .abstract import AbstractElementModel, AbstractModelSerializer


class DataclassSerializer(AbstractModelSerializer[Any]):
    def serialize(self, element: Any) -> AbstractElementModel[Any]:
        return self.field_type(type(element)).serialize(element)

    def field_type(self, element_type: Type[Any]) -> Type[AbstractElementModel[Any]]:
        from tdm.abstract.json_schema.model import create_model_for_type
        return create_model_for_type(element_type)
