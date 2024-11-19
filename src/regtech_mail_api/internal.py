from fastapi import Request

from regtech_api_commons.api.router_wrapper import Router

from regtech_mail_api.settings import EmailApiSettings
from regtech_mail_api.models import Email
from regtech_mail_api.mailer import create_mailer

settings = EmailApiSettings()

router = Router()


@router.post("/confirmation/send")
async def send_email(request: Request):
    mailer = create_mailer()
    # build email
    to_list = ["contact email", "signer email"]
    email = Email("Subject", "Body", settings.from_addr, to=to_list)
    mailer.send(email)
    return "Called internal send"
