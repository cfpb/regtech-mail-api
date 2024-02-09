from pydantic import SecretStr, ValidationError
import pytest

from regtech_mail_api.settings import EmailApiSettings, EmailMailerType


class TestEmailApiSettings:

    default_host = "localhost.localdomain"
    default_from_addr = "noreply@localhost.localdomain"
    default_to = "jane.doe@localhost.localdomain"
    default_smtp_username = SecretStr("tester_1")
    default_smtp_password = SecretStr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_check_smtp_mock_sender(self):
        EmailApiSettings(
            email_mailer=EmailMailerType.MOCK,
            from_addr=self.default_from_addr,
            to=self.default_to,
        )

    def test_check_smtp_no_host(self):
        with pytest.raises(ValidationError) as excinfo:
            EmailApiSettings(
                email_mailer=EmailMailerType.SMTP,
                from_addr=self.default_from_addr,
                to=self.default_to,
            )

        assert "SMTP host must be set when using SMTP email sender" in str(
            excinfo.value
        )

    def test_check_smtp_with_host(self):
        EmailApiSettings(
            email_mailer=EmailMailerType.SMTP,
            smtp_host=self.default_host,
            from_addr=self.default_from_addr,
            to=self.default_to,
        )

    def test_check_smtp_with_creds(self):
        EmailApiSettings(
            email_mailer=EmailMailerType.SMTP,
            smtp_host=self.default_host,
            smtp_username=self.default_smtp_username,
            smtp_password=self.default_smtp_password,
            from_addr=self.default_from_addr,
            to=self.default_to,
        )

    def test_check_smtp_with_creds_no_username(self):
        with pytest.raises(ValidationError) as excinfo:
            EmailApiSettings(
                email_mailer=EmailMailerType.SMTP,
                smtp_host=self.default_host,
                smtp_password=self.default_smtp_password,
                from_addr=self.default_from_addr,
                to=self.default_to,
            )

        assert (
            "username and password must both be set when using SMTP credentials"
            in str(excinfo.value)
        )

    def test_check_smtp_with_creds_no_password(self):
        with pytest.raises(ValidationError) as excinfo:
            EmailApiSettings(
                email_mailer=EmailMailerType.SMTP,
                smtp_host=self.default_host,
                smtp_username=self.default_smtp_username,
                from_addr=self.default_from_addr,
                to=self.default_to,
            )
        assert (
            "username and password must both be set when using SMTP credentials"
            in str(excinfo.value)
        )
