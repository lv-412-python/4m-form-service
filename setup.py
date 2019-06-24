""" app runner """
from form_service import APP  # pylint: disable=cyclic-import


if __name__ == '__main__':
    APP.run(debug=True)
