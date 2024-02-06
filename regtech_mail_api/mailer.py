from abc import ABC
from dataclasses import dataclass

import smtplib
import ssl

from regtech_mail_api.models import Email


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
