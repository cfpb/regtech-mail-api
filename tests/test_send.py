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
def user_no_profile_mock(auth_mock: Mock) -> Mock:
    claims = {
        "email": "test@cfpb.gov",
    }
    auth_mock.return_value = (
        AuthCredentials(["authenticated"]),
        AuthenticatedUser.from_claim(claims),
    )
    return auth_mock


@pytest.fixture
def full_user_mock(auth_mock: Mock) -> Mock:
    claims = {
        "name": "Test User",
        "email": "test@cfpb.gov",
    }
    auth_mock.return_value = (
        AuthCredentials(["authenticated"]),
        AuthenticatedUser.from_claim(claims),
    )
    return auth_mock


class TestEmailApiSend:

    def test_send_no_profile(
        self, mocker: MockerFixture, app_fixture: FastAPI, user_no_profile_mock: Mock
    ):
        email_json = {
            "email": {
                "subject": "Institution Profile Change",
                "body": "lei: 1234567890ABCDEFGHIJ\ninstitution_name_1: Fintech 1\ntin_1: 12-3456789\nrssd_1: 1234567",
                "from_addr": "test@cfpb.gov",
                "sender": "<test@cfpb.gov>",
                "to": ["cases@localhost.localdomain"],
                "cc": None,
                "bcc": None,
            }
        }
        
        client = TestClient(app_fixture)
        res = client.post(
            "/send",
            headers={
                "X-Mail-Subject": "Institution Profile Change",
            },
            data={
                "lei": "1234567890ABCDEFGHIJ",
                "institution_name_1": "Fintech 1",
                "tin_1": "12-3456789",
                "rssd_1": "1234567",
            },
        )
        assert res.status_code == 200
        assert res.json() == email_json

    def test_send(
        self, mocker: MockerFixture, app_fixture: FastAPI, full_user_mock: Mock
    ):
        email_json = {
            "email": {
                "subject": "Institution Profile Change",
                "body": "lei: 1234567890ABCDEFGHIJ\ninstitution_name_1: Fintech 1\ntin_1: 12-3456789\nrssd_1: 1234567",
                "from_addr": "test@cfpb.gov",
                "sender": "Test User <test@cfpb.gov>",
                "to": ["cases@localhost.localdomain"],
                "cc": None,
                "bcc": None,
            }
        }
        
        client = TestClient(app_fixture)
        res = client.post(
            "/send",
            headers={
                "X-Mail-Subject": "Institution Profile Change",
            },
            data={
                "lei": "1234567890ABCDEFGHIJ",
                "institution_name_1": "Fintech 1",
                "tin_1": "12-3456789",
                "rssd_1": "1234567",
            },
        )
        assert res.status_code == 200
        assert res.json() == email_json