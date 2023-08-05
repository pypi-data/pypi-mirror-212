from autoapi.serializers.interface import ISerializer
from autoapi.schema.data import Annotation


class Serializer(ISerializer):

    def serialize(self, content: str | list | dict, annotation: Annotation) -> any:
        for parser in self.content_parsers:
            if parser.check(annotation):
                return parser.serialize(content, annotation)

        raise ValueError(f'Cannot serialize {annotation}: no parser :(')

    def deserialize(self, content: str | list | dict, annotation: Annotation) -> any:
        for parser in self.content_parsers:
            if parser.check(annotation):
                return parser.deserialize(content, annotation)

        raise ValueError(f'Cannot deserialize {annotation}: no parser :(')
