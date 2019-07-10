"""Form view implementation."""  # pylint: disable=cyclic-import
from flask import request, Response, jsonify
from flask_api import status
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import DataError, IntegrityError

from form_service import API
from form_service import APP
from form_service.db import DB
from form_service.models.form import Form
from form_service.serializers.form_schema import FORM_SCHEMA, FORMS_SCHEMA


class FormResource(Resource):
    """Class FormView implementation."""
    def get(self, form_id=None, owner=None):
        """Get method."""
        resp = Response()
        if not owner and not form_id:
            all_forms = Form.query.all()
            message = FORMS_SCHEMA.dump(all_forms).data
            resp = jsonify(message)
            resp.status_code = status.HTTP_200_OK

        elif owner and not form_id:
            owner_forms = Form.query.filter_by(owner=owner).all()
            message = FORMS_SCHEMA.dump(owner_forms).data
            resp = jsonify(message)
            resp.status_code = status.HTTP_200_OK

        else:
            form = Form.query.get(form_id)
            message = FORM_SCHEMA.dump(form).data
            resp = jsonify(message)
            resp.status_code = status.HTTP_200_OK
        return resp

    def delete(self, form_id):
        """Delete method for one form by one user."""
        try:
            form_to_delete = Form.query.get(form_id)
        except DataError as err:
            APP.logger.error(err.args)
            return {'error': 'Invalid url.'}, status.HTTP_404_NOT_FOUND
        if not form_to_delete:
            APP.logger.error('Form with id {} does not exist.'.format(form_id))
            return {'error': 'Does not exist.'}, status.HTTP_400_BAD_REQUEST

        DB.session.delete(form_to_delete)
        DB.session.commit()
        return Response(status=status.HTTP_200_OK)

    def put(self, form_id):
        """Put method for one form by one owner."""
        updated_form = Form.query.get(form_id)
        if not updated_form:
            return {"error": "Does not exist."}, status.HTTP_400_BAD_REQUEST
        try:
            updated_data = FORM_SCHEMA.load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST

        for key, value in updated_data.items():
            setattr(updated_form, key, value)
        try:
            DB.session.commit()
        except IntegrityError as err:
            APP.logger.error(err.args)
            return {'error': 'Already exists.'}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_200_OK)

    def post(self):
        """Post method for Form."""
        try:
            new_form = FORM_SCHEMA.load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST

        add_new_form = Form(**new_form)

        DB.session.add(add_new_form)

        try:
            DB.session.commit()
        except IntegrityError as err:
            APP.logger.error(err.args)
            DB.session.rollback()
            return {'error': 'Already exists.'}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_201_CREATED)


API.add_resource(FormResource, '/form/<form_id>')
