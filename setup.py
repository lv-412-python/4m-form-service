""" app runner """
from form_service import APP  # pylint: disable=cyclic-import


if __name__ == '__main__':
    if not APP.debug:
        from logging.config import fileConfig

        fileConfig('logging.config')

    APP.run()
