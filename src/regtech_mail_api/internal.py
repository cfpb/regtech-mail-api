from datetime import datetime
from fastapi import Request
from pydantic import BaseModel, ConfigDict, EmailStr
from textwrap import dedent
from zoneinfo import ZoneInfo

from regtech_api_commons.api.router_wrapper import Router

from regtech_mail_api.settings import EmailApiSettings
from regtech_mail_api.models import Email
from regtech_mail_api.mailer import create_mailer, get_header

settings = EmailApiSettings()

router = Router()


class ConfirmationRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contact_email: EmailStr
    signer_email: EmailStr
    signer_name: str
    timestamp: datetime
    confirmation_id: str


body_template = """
    Congratulations! This email confirms that the filing submitted by {signer_name} on {formatted_date} was successful. The confirmation number is {confirmation_id}.

    To make any changes to the filing, please return to the Small Business Lending Data Filing Platform and follow the provided instructions. If you have any questions or need additional support, email our support staff at sblhelp@cfpb.gov.
"""


@router.post("/confirmation/send")
async def send_email(request: Request, confirmation_request: ConfirmationRequest):
    mailer = create_mailer()

    timestamp_est = confirmation_request.timestamp.astimezone(
        ZoneInfo("America/New_York")
    )
    formatted_date = timestamp_est.strftime("%B %d, %Y at %-I:%M %p %Z")
    body_text = dedent(
        body_template.format(
            signer_name=confirmation_request.signer_name,
            formatted_date=formatted_date,
            confirmation_id=confirmation_request.confirmation_id,
        )
    )

    to_list = [confirmation_request.contact_email, confirmation_request.signer_email]
    email = Email(
        f"{get_header(confirmation_request.signer_email)} Small Business Lending Data Filing Confirmation",
        body_text,
        settings.from_addr,
        to=to_list,
    )
    mailer.send(email)
    return {"email": email}
