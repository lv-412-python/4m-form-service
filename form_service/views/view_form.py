"""Form view implementation."""
from flask_restful import Resource
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from form_service import API
from form_service.db import DB
from form_service.models.form import Form
from form_service.serializers.form_schema import FORM_SCHEMA, FORMS_SCHEMA


class OwnerForm(Resource):
    """Class OwnerForm view implementation."""
    def get(self, form_id):  # pylint: disable=no-self-use
        """Get method for one form by one owner."""
        try:
            form = Form.query.get(form_id)
        except IntegrityError:
            return jsonify({'message': 'Form with this id, by this user could not be found.'}), 400
        output = FORM_SCHEMA.dump(form).data
        return jsonify(output)

    def put(self, form_id):  # pylint: disable=no-self-use
        """Put method for one form by one owner."""
        updated_form = Form.query.get(form_id)

        title = request.json['title']
        description = request.json['description']
        owner = request.json['owner']

        updated_form.title = title
        updated_form.description = description
        updated_form.owner = owner

        DB.session.commit()  # pylint: disable=no-member

        return FORM_SCHEMA.jsonify(updated_form)

    def delete(self, form_id):  # pylint: disable=no-self-use
        """Delete method for one form by one user."""
        form_to_delete = Form.query.get(form_id)

        DB.session.delete(form_to_delete)  # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member

        return FORM_SCHEMA.jsonify(form_to_delete)


class EveryForm(Resource):
    """Class EveryForm view implementation."""
    def get(self, owner):  # pylint: disable=no-self-use
        """Get method for all form by one owner."""
        try:
            all_forms = Form.query.filter_by(owner=owner)
        except IntegrityError:
            return jsonify({'message': 'Forms by this user could not be found.'}), 400
        output = FORMS_SCHEMA.dump(all_forms).data
        return jsonify(output)


class NewForm(Resource):
    """Class NewForm implementation."""
    def post(self):  # pylint: disable=no-self-use
        """Post method for Form."""
        title = request.json['title']
        description = request.json['description']
        owner = request.json['owner']

        exists = bool(
            Form.query.filter_by(title=title, description=description, owner=owner).first())

        if exists:
            result = {'error': 'this form already exists.'}
        else:
            new_form = Form(title, description, owner)

            DB.session.add(new_form)  # pylint: disable=no-member
            DB.session.commit()  # pylint: disable=no-member

            result = FORM_SCHEMA.jsonify(new_form)

        return result


API.add_resource(OwnerForm, '/form/<form_id>')
API.add_resource(EveryForm, '/forms/<owner>')
API.add_resource(NewForm, '/form/new')
