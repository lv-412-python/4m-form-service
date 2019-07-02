"""Form view implementation."""  # pylint: disable=cyclic-import
from flask_restful import Resource
from flask import request, Response
from form_service import API
from form_service.db import DB
from form_service.models.form import Form
from form_service.serializers.form_schema import FORM_SCHEMA, FORMS_SCHEMA


class OwnerForm(Resource):
    """Class OwnerForm view implementation."""
    def get(self, form_id):  # pylint: disable=no-self-use
        """Get method for one form by one owner."""
        if form_id.isnumeric():
            form = Form.query.filter_by(form_id=form_id)
            output = FORMS_SCHEMA.dump(form).data
            if not output:
                output = {'message': 'Form with this id could not be found.'}, 400
        return output

    def put(self, form_id):  # pylint: disable=no-self-use
        """Put method for one form by one owner."""
        updated_form = Form.query.get(form_id)

        title = request.json['title']
        description = request.json['description']
        owner = request.json['owner']

        updated_form.title = title
        updated_form.description = description
        updated_form.owner = owner

        DB.session.commit()

        return FORM_SCHEMA.jsonify(updated_form)

    def delete(self, form_id):  # pylint: disable=no-self-use
        """Delete method for one form by one user."""
        if form_id.isnumeric():
            form_to_delete = Form.query.get(form_id)
            if not form_to_delete:
                return {"message": "Form does not exist."}, 400

        DB.session.delete(form_to_delete)
        DB.session.commit()
        return Response(status=200)


class EveryForm(Resource):
    """Class EveryForm view implementation."""
    def get(self, owner):  # pylint: disable=no-self-use
        """Get method for all form by one owner."""
        if owner.isnumeric():
            all_forms = Form.query.filter_by(owner=owner)
            output = FORMS_SCHEMA.dump(all_forms).data
            if not output:
                output = {'message': 'Forms by this user could not be found.'}, 400
        return output


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
            message = {'error': 'this form already exists.'}, 400
        else:
            new_form = Form(title=title, description=description, owner=owner, form_id=1)

            DB.session.add(new_form)
            DB.session.commit()

        return message if exists else FORM_SCHEMA.jsonify(new_form)


API.add_resource(OwnerForm, '/form/<form_id>')
API.add_resource(EveryForm, '/forms/<owner>')
API.add_resource(NewForm, '/form/new')
