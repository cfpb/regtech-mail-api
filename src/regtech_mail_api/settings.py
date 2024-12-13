from enum import Enum
from pydantic import EmailStr, SecretStr, model_validator
from pydantic_settings import BaseSettings

from regtech_api_commons.oauth2.config import KeycloakSettings


class EmailMailerType(str, Enum):
    MOCK = "mock"
    SMTP = "smtp"


class EmailApiSettings(BaseSettings):
    environment: str = ""
    email_mailer: EmailMailerType = EmailMailerType.SMTP
    smtp_host: str | None = None
    smtp_port: int = 0
    smtp_username: SecretStr | None = None
    smtp_password: SecretStr | None = None
    smtp_use_tls: bool = False
    from_addr: EmailStr
    to: EmailStr
    cc: set[EmailStr] | None = None
    bcc: set[EmailStr] | None = None

    prod_body_template: str = None
    beta_body_template: str = None

    @model_validator(mode="after")
    def check_smtp(self):
        if self.email_mailer == EmailMailerType.SMTP:

            if self.smtp_host:
                if bool(self.smtp_username) ^ bool(self.smtp_password):
                    raise ValueError(
                        "username and password must both be set when using SMTP credentials"
                    )
            else:
                raise ValueError("SMTP host must be set when using SMTP email sender")

        return self


kc_settings = KeycloakSettings()
