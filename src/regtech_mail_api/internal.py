from datetime import datetime
from fastapi import Request
from pydantic import BaseModel, ConfigDict, EmailStr
from textwrap import dedent
from zoneinfo import ZoneInfo

from regtech_api_commons.api.router_wrapper import Router

from regtech_mail_api.settings import EmailApiSettings
from regtech_mail_api.models import Email
from regtech_mail_api.mailer import create_mailer

settings = EmailApiSettings()

router = Router()


class ConfirmationRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contact_email: EmailStr
    signer_email: EmailStr
    signer_name: str
    timestamp: datetime
    confirmation_id: str


prod_body_template = """
    Congratulations! This email confirms that the filing submitted by {signer_name} on {formatted_date} was successful. The confirmation number is {confirmation_id}.

    To make any changes to the filing, please return to the Small Business Lending Data Filing Platform and follow the provided instructions. If you have any questions or need additional support, email our support staff at sblhelp@cfpb.gov.
"""

beta_body_template = """
    Congratulations! This email confirms that the filing submitted by {signer_name} on {formatted_date} was successful. The confirmation number is {confirmation_id}.

    The beta platform is for testing purposes only and user-supplied data may be removed at any time. Take a moment to email our support staff at sblhelp@cfpb.gov with your feedback or upload a new file to continue testing.
"""


@router.post("/confirmation/send")
async def send_email(request: Request, confirmation_request: ConfirmationRequest):
    mailer = create_mailer()

    timestamp_est = confirmation_request.timestamp.astimezone(
        ZoneInfo("America/New_York")
    )
    formatted_date = timestamp_est.strftime("%B %d, %Y at %-I:%M %p %Z")
    body_template = (
        prod_body_template if settings.environment == "PROD" else beta_body_template
    )
    body_text = dedent(
        body_template.format(
            signer_name=confirmation_request.signer_name,
            formatted_date=formatted_date,
            confirmation_id=confirmation_request.confirmation_id,
        )
    )

    to_list = (
        [confirmation_request.contact_email, confirmation_request.signer_email]
        if settings.environment == "PROD"
        else [confirmation_request.signer_email]
    )
    header = "" if settings.environment == "PROD" else "[BETA] "
    email = Email(
        f"{header}Small Business Lending Data Filing Confirmation",
        body_text,
        settings.from_addr,
        to=to_list,
    )
    mailer.send(email)
    return {"email": email}
