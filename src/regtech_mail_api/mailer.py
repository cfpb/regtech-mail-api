from abc import ABC
from dataclasses import dataclass

import smtplib
import ssl

from regtech_mail_api.models import Email
from regtech_mail_api.settings import EmailApiSettings, EmailMailerType


class Mailer(ABC):

    def send(self, message: Email) -> None:
        pass


@dataclass
class SmtpMailer(Mailer):

    host: str
    port: int = 0
    username: str | None = None
    password: str | None = None
    use_tls: bool = False

    # TODO: Consider moving connection and login functionality into __init__,
    #       BUT we'll need to make sure it can gracefully recover if a
    #       connection is broken.
    def send(self, message: Email) -> None:
        mailer = smtplib.SMTP(host=self.host, port=self.port)

        if self.use_tls:
            mailer.starttls(context=ssl.create_default_context())

        if self.username and self.password:
            mailer.login(self.username, self.password)

        mailer.send_message(msg=message.to_email_message())
        mailer.quit()


class MockMailer(Mailer):

    def send(self, message: Email) -> None:
        print("--- Message Start ---")
        print(message.to_email_message())
        print("--- Message End ---")


def create_mailer():
    settings = EmailApiSettings()  # type: ignore
    mailer: Mailer

    match settings.email_mailer:
        case EmailMailerType.SMTP:
            mailer = SmtpMailer(
                settings.smtp_host,  # type: ignore
                settings.smtp_port,
                settings.smtp_username.get_secret_value() if settings.smtp_username else None,  # type: ignore
                settings.smtp_password.get_secret_value() if settings.smtp_password else None,  # type: ignore
                settings.smtp_use_tls,
            )
        case EmailMailerType.MOCK:
            mailer = MockMailer()
        case _:
            raise ValueError(f"Mailer type {settings.email_mailer} not supported")

    return mailer


def get_header(email):
    settings = EmailApiSettings()  # type: ignore
    header = "[BETA]"
    if "cfpb" in email.lower().split("@")[-1]:
        header = "[CFPB BETA]"
    if settings.environment:
        header = f"[{settings.environment}]"
        if settings.environment == "PROD":
            header = ""
    return header
