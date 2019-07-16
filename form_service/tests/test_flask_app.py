"""Tests for form service."""
from unittest import main
from unittest.mock import patch

from flask_testing import TestCase
from marshmallow import ValidationError

from form_service import APP
from form_service.config.test_config import TestConfiguration
from form_service.db import DB
from form_service.models.form import Form


def create_app(config_obj):
    """
    Creates Flask app with configuration, you need.
    :param config_obj: name of configuration.
    :return: flask app.
    """
    app = APP
    app.config.from_object(config_obj)
    return app


class GetPutDeleteTest(TestCase):
    """Tests for get, put and delete resources with the same set-up."""

    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        form1 = Form(title="Test", description="testing.", owner=2, fields="1, 4, 8, 9, 6")
        form2 = Form(title="Another test", description="new one", owner=2, fields="4, 7, 8, 9, 1")
        DB.session.add(form1)
        DB.session.add(form2)
        DB.session.commit()
        id1 = Form.query.filter_by(title="Test", description="testing.",
                                   owner=2, fields="1, 4, 8, 9, 6").first()
        self.owner_id_1 = id1.owner
        self.forms_id_1 = id1.form_id
        id2 = Form.query.filter_by(title="Another test", description="new one",
                                   owner=2, fields="4, 7, 8, 9, 1").first()
        self.owner_id_2 = id2.owner
        self.forms_id_2 = id2.form_id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get_all_forms_by_one_owner(self):
        """Tests get method to get all forms."""
        with self.create_app().test_client() as client:
            response = client.get('/form?owner=2')
            check = [{
                "title": "Test",
                "description": "testing.",
                "owner": self.owner_id_1,
                "form_id": self.forms_id_1,
                "fields": [1, 4, 8, 9, 6]
            }, {
                "title": "Another test",
                "description": "new one",
                "owner": self.owner_id_2,
                "form_id": self.forms_id_2,
                "fields": [4, 7, 8, 9, 1]
            }]
            self.assertEqual(response.json, check)

    def test_get_one_form(self):
        """Tests get method to get one particular form."""
        with self.create_app().test_client() as client:
            response = client.get('/form/{}'.format(self.forms_id_1))
            check = {
                "title": "Test",
                "description": "testing.",
                "owner": 2,
                "form_id": self.forms_id_1,
                "fields": [1, 4, 8, 9, 6]
            }
            self.assertEqual(response.json, check)

    def test_get_no_data(self):
        """Tests get method with id that does not exist."""
        with self.create_app().test_client() as client:
            response = client.get('/form/123464367')
            self.assertEqual(response.json, {'error': 'Does not exist.'})

    def test_put(self):
        """Tests put method."""
        with self.create_app().test_client() as client:
            new = {
                "title": "Test",
                "description": "testing.",
                "owner": 5,
                "fields": [1, 4, 8, 9, 6]
            }
            response = client.put('/form/{}'.format(self.forms_id_1), json=new)
            self.assertEqual(response.status_code, 200)

    def test_put_no_form(self):
        """Tests put method."""
        with self.create_app().test_client() as client:
            response = client.put('/form/13575836')
            self.assertEqual(response.json, {'error': 'Does not exist.'})

    def test_delete(self):
        """Tests delete method."""
        with self.create_app().test_client() as client:
            response = client.delete('/form/{}'.format(self.forms_id_1))
            form = Form.query.filter_by(form_id=self.forms_id_1).first()
            self.assertEqual(form, None)
            self.assertEqual(response.status_code, 200)

    def test_delete_no_data(self):
        """Tests delete method is the form with that id does not exist"""
        with self.create_app().test_client() as client:
            response = client.delete('/form/123')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['error'], 'Does not exist.')


class PostTest(TestCase):
    """Tests for post method."""

    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables."""
        DB.create_all()

    def test_post_success(self):
        """Tests post resource success."""
        with self.create_app().test_client() as client:
            response = client.post('/form',
                                   json={"title": "Test", "description": "testing.",
                                         "owner": 2, "fields": [14896]})
            self.assertEqual(response.status_code, 201)

    def test_post_failure(self):
        """Tests post resource failure."""
        with self.create_app().test_client() as client:
            client.post('/form', json={"title": "Test", "description": "testing.",
                                       "owner": 2, "fields": [14896]})
            response = client.post('/form',
                                   json={"title": "Test", "description": "testing.",
                                         "owner": 2, "fields": [14896]})
            self.assertEqual(response.status_code, 400)

    @patch('form_service.models.form.Form.query', **{'get.side_effect': ValidationError(None)})
    def test_post_validation_error(self, mock_obj):  # pylint: disable=unused-argument
        """Tests post method for ValidationError."""
        with self.create_app().test_client() as client:
            response = client.post('/form',
                                   json={"title": 1, "description": "testing.",
                                         "owner": 2, "fields": [14896]})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['title'], ['Not a valid string.'])

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()


if __name__ == '__main__':
    main()
