"""Model for form service."""
from sqlalchemy import Column, Integer, String, Text, UniqueConstraint

from form_service.db import DB


class Form(DB.Model):
    """Implementation of Form entity."""
    form_id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(Integer())
    fields = Column(String(100))
    __table_args__ = (UniqueConstraint(title, owner, fields),)
