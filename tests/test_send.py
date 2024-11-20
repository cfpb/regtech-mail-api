import json
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from unittest.mock import Mock

from regtech_api_commons.models.auth import AuthenticatedUser
from starlette.authentication import AuthCredentials


@pytest.fixture
def app_fixture(mocker: MockerFixture) -> FastAPI:
    from regtech_mail_api.api import app

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
        "preferred_username": "testuser",
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
        "preferred_username": "testuser",
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
                "subject": "[CFPB BETA] SBL User Request for Institution Profile Change",
                "body": "Contact Email: test@cfpb.gov\nContact Name: \n\nlei: 1234567890ABCDEFGHIJ\ninstitution_name_1: Fintech 1\ntin_1: 12-3456789\nrssd_1: 1234567",
                "from_addr": "test@cfpb.gov",
                "to": ["cases@localhost.localdomain"],
                "cc": None,
                "bcc": None,
            }
        }

        client = TestClient(app_fixture)
        res = client.post(
            "/public/case/send",
            headers={
                "case-type": "Institution Profile Change",
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

    def test_case_send(
        self, mocker: MockerFixture, app_fixture: FastAPI, full_user_mock: Mock
    ):
        email_json = {
            "email": {
                "subject": "[CFPB BETA] SBL User Request for Institution Profile Change",
                "body": "Contact Email: test@cfpb.gov\nContact Name: Test User\n\nlei: 1234567890ABCDEFGHIJ\ninstitution_name_1: Fintech 1\ntin_1: 12-3456789\nrssd_1: 1234567",
                "from_addr": "test@cfpb.gov",
                "to": ["cases@localhost.localdomain"],
                "cc": None,
                "bcc": None,
            }
        }

        client = TestClient(app_fixture)
        res = client.post(
            "/public/case/send",
            headers={
                "case-type": "Institution Profile Change",
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

    def test_confirmation_send(
        self, mocker: MockerFixture, app_fixture: FastAPI, full_user_mock: Mock
    ):
        client = TestClient(app_fixture)
        res = client.post(
            "/internal/confirmation/send",
            data=json.dumps(
                {
                    "confirmation_id": "test",
                    "signer_email": "test@cfpb.gov",
                    "signer_name": "Test User",
                    "contact_email": "test_contact@cfpb.gov",
                    "timestamp": 1732128696,
                }
            ),
        )

        expected_email = {
            "subject": "[CFPB BETA] Small Business Lending Data Filing Confirmation",
            "body": "\nCongratulations! This email confirms that the filing submitted by Test User on November 20, 2024 at 1:51 PM EST was successful. The confirmation number is test.\n\nTo make any changes to the filing, please return to the Small Business Lending Data Filing Platform and follow the provided instructions. If you have any questions or need additional support, email our support staff at sblhelp@cfpb.gov.\n",
            "from_addr": "test@cfpb.gov",
            "to": ["test_contact@cfpb.gov", "test@cfpb.gov"],
            "cc": None,
            "bcc": None,
        }

        assert res.status_code == 200
        assert res.json()["email"] == expected_email
