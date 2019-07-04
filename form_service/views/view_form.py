"""Form view implementation."""  # pylint: disable=cyclic-import
from flask_restful import Resource
from flask import request, Response
from sqlalchemy.exc import DataError
from form_service import API
from form_service.db import DB
from form_service.models.form import Form
from form_service.serializers.form_schema import FORM_SCHEMA, FORMS_SCHEMA


class OwnerForm(Resource):
    """Class OwnerForm view implementation."""

    def put(self, form_id):  # pylint: disable=no-self-use
        """Put method for one form by one owner."""
        try:
            updated_form = Form.query.get(form_id)
        except DataError:
            return {'message': 'Invalid url.'}, 400
        if not updated_form:
            return {'message': 'Form with this id could not be found.'}, 400

        updated_form.title = request.json['title']
        updated_form.description = request.json['description']
        updated_form.owner = request.json['owner']

        DB.session.commit()
        output = FORM_SCHEMA.jsonify(updated_form)
        return output

    def delete(self, form_id):  # pylint: disable=no-self-use
        """Delete method for one form by one user."""
        try:
            form_to_delete = Form.query.get(form_id)
        except DataError:
            return {"message": "Form does not exist."}, 400

        DB.session.delete(form_to_delete)
        DB.session.commit()
        return Response(status=200)

    def get(self, form_id):  # pylint: disable=no-self-use
        """Get method for one form by one owner."""
        try:
            form = Form.query.get(form_id)
        except DataError:
            return {'message': 'Invalid url.'}, 400
        if not form:
            return {'message': 'Form with this id could not be found.'}, 400
        form = FORM_SCHEMA.dump(form).data
        return form, 200


class EveryForm(Resource):
    """Class EveryForm view implementation."""
    def get(self, owner):  # pylint: disable=no-self-use
        """Get method for all form by one owner."""
        try:
            if owner.isnumeric():
                all_forms = Form.query.filter_by(owner=owner)
            else:
                return {'message': 'Invalid url.'}, 400
        except DataError:
            return {'message': 'Invalid url.'}, 400
        for form in all_forms:
            form.fields = list(map(int, form.fields.split(',')))
        all_forms = FORMS_SCHEMA.dump(all_forms).data
        if not all_forms:
            return {'message': 'Forms by this user could not be found.'}, 400

        return all_forms


class NewForm(Resource):
    """Class NewForm implementation."""
    def post(self):  # pylint: disable=no-self-use
        """Post method for Form."""
        title = request.json['title']
        description = request.json['description']
        owner = request.json['owner']
        fields = request.json['fields']

        fields = ",".join(map(str, fields))

        try:
            exists = bool(
                Form.query.filter_by(title=title, description=description, owner=owner,
                                     fields=fields).first())
        except DataError:
            return {'message': 'Invalid data.'}, 400

        if exists:
            message = {'error': 'This form already exists.'}, 400
        else:
            new_form = Form(title=title, description=description, owner=owner,
                            fields=fields)

            DB.session.add(new_form)
            DB.session.commit()

        return message if exists else FORM_SCHEMA.jsonify(new_form)


API.add_resource(OwnerForm, '/form/<form_id>')
API.add_resource(EveryForm, '/forms/<owner>')
API.add_resource(NewForm, '/form/new')
