"""Schemas for Form service."""
import marshmallow
from marshmallow import post_load, pre_dump
from form_service import MA


class FormSchema(MA.Schema):
    """Implementation of Form schema."""
    form_id = marshmallow.fields.Integer(dump_only=True)
    title = marshmallow.fields.String()
    description = marshmallow.fields.String()
    owner = marshmallow.fields.Integer()
    fields = marshmallow.fields.List(marshmallow.fields.Integer())

    @post_load
    def convert_list_from_str(self, data):
        """Converts into list from string."""
        if 'fields' in data:
            data['fields'] = ",".join(map(str, data['fields']))
        return data

    @pre_dump
    def convert_str_from_list(self, data):
        """Converts into string from list."""
        data.fields = list(map(int, data.fields.split(',')))
        return data


FORM_SCHEMA = FormSchema(strict=True)
FORMS_SCHEMA = FormSchema(many=True, strict=True)
