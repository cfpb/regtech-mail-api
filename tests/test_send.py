import json
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from unittest.mock import Mock

from regtech_api_commons.models.auth import AuthenticatedUser
from starlette.authentication import AuthCredentials

from datetime import datetime, timezone


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

    def test_email_dates(
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
                    "timestamp": datetime(
                        2024, 3, 15, 10, 10, tzinfo=timezone.utc
                    ).timestamp()
                    * 1000,
                }
            ),
        )

        expected_email = {
            "subject": "[BETA] Small Business Lending Data Filing Confirmation",
            "body": "Congratulations! This email confirms that Test User submitted a filing on March 15, 2024 at 6:10 a.m. EST. The confirmation number for this filing is test.\n\nYou filed in beta.",
            "from_addr": "test@cfpb.gov",
            "to": ["test@cfpb.gov"],
            "cc": None,
            "bcc": None,
        }

        assert res.status_code == 200
        assert res.json()["email"] == expected_email

        res = client.post(
            "/internal/confirmation/send",
            data=json.dumps(
                {
                    "confirmation_id": "test",
                    "signer_email": "test@cfpb.gov",
                    "signer_name": "Test User",
                    "contact_email": "test_contact@cfpb.gov",
                    "timestamp": datetime(
                        2024, 9, 15, 17, 10, tzinfo=timezone.utc
                    ).timestamp()
                    * 1000,
                }
            ),
        )

        expected_email = {
            "subject": "[BETA] Small Business Lending Data Filing Confirmation",
            "body": "Congratulations! This email confirms that Test User submitted a filing on Sept. 15, 2024 at 1:10 p.m. EST. The confirmation number for this filing is test.\n\nYou filed in beta.",
            "from_addr": "test@cfpb.gov",
            "to": ["test@cfpb.gov"],
            "cc": None,
            "bcc": None,
        }

        assert res.status_code == 200
        assert res.json()["email"] == expected_email

    def test_confirmation_send(
        self,
        mocker: MockerFixture,
        app_fixture: FastAPI,
        full_user_mock: Mock,
        monkeypatch,
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
            "subject": "[BETA] Small Business Lending Data Filing Confirmation",
            "body": "Congratulations! This email confirms that Test User submitted a filing on Nov. 20, 2024 at 1:51 p.m. EST. The confirmation number for this filing is test.\n\nYou filed in beta.",
            "from_addr": "test@cfpb.gov",
            "to": ["test@cfpb.gov"],
            "cc": None,
            "bcc": None,
        }

        assert res.status_code == 200
        assert res.json()["email"] == expected_email

        monkeypatch.setattr("regtech_mail_api.internal.settings.environment", "PROD")
        expected_email = {
            "subject": "Small Business Lending Data Filing Confirmation",
            "body": "Congratulations! This email confirms that Test User submitted a filing on Nov. 20, 2024 at 1:51 p.m. EST was successful. The confirmation number for this filing is test.\n\nYou filed in PROD.",
            "from_addr": "test@cfpb.gov",
            "to": ["test_contact@cfpb.gov", "test@cfpb.gov"],
            "cc": None,
            "bcc": None,
        }

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

        assert res.status_code == 200
        assert res.json()["email"] == expected_email
