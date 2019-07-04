"""Model for form service."""
from sqlalchemy import Column, Integer, String, Text
from form_service.db import DB


class Form(DB.Model):  # pylint: disable=too-few-public-methods
    """Implementation of Form entity."""
    form_id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(Integer())
