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

custom_months = {
    "January": "Jan.",
    "February": "Feb.",
    "August": "Aug.",
    "September": "Sept.",
    "October": "Oct.",
    "November": "Nov.",
    "December": "Dec.",
}


class ConfirmationRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contact_email: EmailStr
    signer_email: EmailStr
    signer_name: str
    timestamp: datetime
    confirmation_id: str


@router.post("/confirmation/send")
async def send_email(request: Request, confirmation_request: ConfirmationRequest):
    mailer = create_mailer()

    timestamp_est = confirmation_request.timestamp.astimezone(
        ZoneInfo("America/New_York")
    )
    full_month = timestamp_est.strftime("%B")
    formatted_month = custom_months.get(full_month, full_month)
    am_pm = "a.m." if timestamp_est.strftime("%p") == "AM" else "p.m."
    formatted_date = (
        f"{formatted_month} {timestamp_est.strftime("%d, %Y at %-I:%M")} {am_pm} EST"
    )
    body_template = (
        settings.prod_body_template
        if settings.environment == "PROD"
        else settings.beta_body_template
    )
    body_text = dedent(
        body_template.format(
            signer_name=confirmation_request.signer_name,
            formatted_date=formatted_date,
            confirmation_id=confirmation_request.confirmation_id,
            line_break="\n\n",
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
