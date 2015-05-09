from schemalite import Schema, Field, validator
from schemalite.validators import type_validator


class StorySchema(Schema):

    title = Field(validator=type_validator(str, unicode))


class SnippetSchema(Schema):

    text = Field(validator=type_validator(str, unicode))

    @validator(text)
    def validate_text_size(data):
        if len(data) < 10:
            return (False, "Snippet shorter than minimum permitted length")
        if len(data) > 50:
            return (False, "Snippet longer than maximum permitted length")
        return (True, None)
