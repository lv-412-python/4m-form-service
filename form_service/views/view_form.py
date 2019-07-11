"""Form view implementation."""  # pylint: disable=cyclic-import
from flask import request, Response, jsonify
from flask_api import status
from flask_restful import Resource, HTTPException
from marshmallow import ValidationError, fields
from sqlalchemy.exc import DataError, IntegrityError
from webargs.flaskparser import parser

from form_service import API
from form_service import APP
from form_service.db import DB
from form_service.models.form import Form
from form_service.serializers.form_schema import FORM_SCHEMA, FORMS_SCHEMA


class FormResource(Resource):
    """Class FormView implementation."""
    def get(self):
        """
        Get method for Form Service.
        :return: requested forms with status code or error message with status code.
        """
        resp = Response()
        ids = {
            'form_id': fields.List(fields.Int(validate=lambda value: value > 0)),
            'owner': fields.List(fields.Int(validate=lambda value: value > 0))
        }
        try:
            ids = parser.parse(ids, request)
        except HTTPException as err:
            APP.logger.error(err.args)
            return {'error': 'Invalid URL.'}, status.HTTP_400_BAD_REQUEST
        output = Form.query.filter()
        if 'form_id' in ids:
            output = output.filter(Form.form_id.in_(ids['form_id']))
        if 'owner' in ids:
            output = output.filter(Form.owner.in_(ids['owner']))
        result = FORMS_SCHEMA.dump(output).data
        resp = jsonify(result)
        resp.status_code = status.HTTP_200_OK

        return resp if result else ({'error': 'Does not exist.'}, status.HTTP_404_NOT_FOUND)

    def delete(self):
        """
        Delete method for the form.
        :return: Response object or error message with status code.
        """
        form_id = request.args.get('form_id')
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

    def put(self):
        """
        Put method for the form.
        :return: Response object or error message with status code.
        """
        form_id = request.args.get('form_id')
        updated_form = Form.query.get(form_id)
        if not updated_form:
            return {'error': 'Does not exist.'}, status.HTTP_400_BAD_REQUEST
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
        """
        Post method for creating a new form.
        :return: Response object or error message with status code.
        """
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


API.add_resource(FormResource, '/form')
