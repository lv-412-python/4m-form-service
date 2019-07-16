""" app runner """
from logging.config import fileConfig

from form_service import APP  # pylint: disable=cyclic-import


if __name__ == '__main__':

    fileConfig('logging.config')

    APP.run(host='0.0.0.0', port=5050)
