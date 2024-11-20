from fastapi import Request
from starlette.authentication import requires

from regtech_api_commons.api.router_wrapper import Router

from regtech_mail_api.settings import EmailApiSettings
from regtech_mail_api.models import Email
from regtech_mail_api.mailer import create_mailer, get_header

settings = EmailApiSettings()

router = Router()


@router.post("/case/send")
@requires("authenticated")
async def send_email(request: Request):
    sender_addr = request.user.email
    sender_name = request.user.name if request.user.name else ""
    type = request.headers["case-type"]

    subject = f"{get_header(sender_addr)} SBL User Request for {type}"

    form_data = await request.form()

    body_lines = [f"{k}: {v}" for k, v in form_data.items()]
    email_body = f"Contact Email: {sender_addr}\n"
    email_body += f"Contact Name: {sender_name}\n\n"
    email_body += "\n".join(body_lines)

    email = Email(subject, email_body, settings.from_addr, to={settings.to})

    create_mailer().send(email)

    return {"email": email}
