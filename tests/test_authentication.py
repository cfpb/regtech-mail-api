import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from unittest.mock import Mock

from regtech_api_commons.models.auth import AuthenticatedUser
from starlette.authentication import AuthCredentials, UnauthenticatedUser


@pytest.fixture
def app_fixture(mocker: MockerFixture) -> FastAPI:
    from api import app

    return app


@pytest.fixture
def auth_mock(mocker: MockerFixture) -> Mock:
    return mocker.patch(
        "regtech_api_commons.oauth2.oauth2_backend.BearerTokenAuthBackend.authenticate"
    )


@pytest.fixture
def authed_user_mock(auth_mock: Mock) -> Mock:
    claims = {
        "name": "Test User",
        "preferred_username": "test_user",
        "email": "test@cfpb.gov",
    }
    auth_mock.return_value = (
        AuthCredentials(["authenticated"]),
        AuthenticatedUser.from_claim(claims),
    )
    return auth_mock


@pytest.fixture
def unauthed_user_mock(auth_mock: Mock) -> Mock:
    auth_mock.return_value = (AuthCredentials("unauthenticated"), UnauthenticatedUser())
    return auth_mock


class TestEmailApiAuthentication:

    def test_unauthed_endpoints(
        self, mocker: MockerFixture, app_fixture: FastAPI, unauthed_user_mock: Mock
    ):
        client = TestClient(app_fixture)
        res = client.get("/")
        assert res.status_code == 403

        client = TestClient(app_fixture)
        res = client.post(
            "/send",
            json={"data": "data"},
        )
        assert res.status_code == 403

    def test_authed_endpoints(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        email_json = {
            "email": {
                "subject": "Institution Profile Change",
                "body": "lei: 1234567890ABCDEFGHIJ\ninstitution_name_1: Fintech 1\ntin_1: 12-3456789\nrssd_1: 1234567",
                "from_addr": "test@cfpb.gov",
                "sender": "Jane Doe <jane.doe@some.org>",
                "to": ["cases@localhost.localdomain"],
                "cc": None,
                "bcc": None,
            }
        }

        mock = mocker.patch("api.send_email")
        mock.return_value = {"email": email_json}
        client = TestClient(app_fixture)
        res = client.get("/")
        assert res.status_code == 200
