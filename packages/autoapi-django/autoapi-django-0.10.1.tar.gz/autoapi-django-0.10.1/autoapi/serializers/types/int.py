from autoapi.serializers.interface import ITypeSerializer
from autoapi.schema.data import Annotation


class IntSerializer(ITypeSerializer):
    def check(self, annotation: Annotation):
        return annotation.type.type is int

    def serialize(self, content: any, annotation: Annotation) -> int:
        if not isinstance(content, int):
            raise ValueError(f'Cannot serialize content = {content} as integer!')
        return content

    def deserialize(self, content: any, annotation: Annotation) -> any:
        return int(content)
