from dataclasses import dataclass
from email.message import EmailMessage


@dataclass
class Email:
    subject: str
    body: str
    from_addr: str
    to: set[str]
    cc: set[str] | None = None
    bcc: set[str] | None = None

    def to_email_message(self) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = self.subject
        message["From"] = self.from_addr
        message["To"] = ",".join(self.to)

        if self.cc:
            message["CC"] = ",".join(self.cc)

        if self.bcc:
            message["BCC"] = ",".join(self.bcc)

        message.set_content(self.body)

        return message
