"""Schemas for Form service."""
from form_service import MA


class FormSchema(MA.Schema):  # pylint: disable=too-few-public-methods
    """Implementation of Form schema."""
    class Meta:  # pylint: disable=too-few-public-methods
        """Implementation of Meta class with fields, we want to show."""
        fields = ('form_id', 'title', 'description', 'owner')


FORM_SCHEMA = FormSchema(strict=True)
FORMS_SCHEMA = FormSchema(many=True, strict=True)
