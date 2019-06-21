"""Models for form service."""
from form_service import DB


class Form(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    title = DB.Column(DB.string(100))
    description = DB.Column(DB.Text)
