import pytest
from flaskr import create_app


@pytest.fixture()
def app():
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield test_app

    # clean up / reset resources here


@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
    return app.test_client()


@pytest.fixture()
def runner(app):  # pylint: disable=redefined-outer-name
    return app.test_cli_runner()
