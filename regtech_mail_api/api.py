from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from regtech_mail_api.mailer import Mailer, MockMailer, SmtpMailer
from regtech_mail_api.models import Email
from regtech_mail_api.settings import EmailApiSettings, EmailMailerType, kc_settings

from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware

from regtech_api_commons.oauth2.oauth2_backend import BearerTokenAuthBackend
from regtech_api_commons.oauth2.oauth2_admin import OAuth2Admin

app = FastAPI()

token_bearer = OAuth2AuthorizationCodeBearer(
    authorizationUrl=kc_settings.auth_url.unicode_string(),
    tokenUrl=kc_settings.token_url.unicode_string(),
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=BearerTokenAuthBackend(token_bearer, OAuth2Admin(kc_settings)),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # thinking this should be derived from an env var from docker-compose or helm values
    allow_methods=["GET", "POST"],
    allow_headers=["authorization"],
)


# FIXME: Come up with a better way of handling these settings
#        without having to do all the `type: ignore`s
settings = EmailApiSettings()  # type: ignore
mailer: Mailer

match settings.email_mailer:
    case EmailMailerType.SMTP:
        mailer = SmtpMailer(
            settings.smtp_host,  # type: ignore
            settings.smtp_port,
            settings.smtp_username,  # type: ignore
            settings.smtp_password,  # type: ignore
            settings.smtp_use_tls,
        )
    case EmailMailerType.MOCK:
        mailer = MockMailer()
    case _:
        raise ValueError(f"Mailer type {settings.email_mailer} not supported")


@app.get("/")
@requires("authenticated")
def read_root(request: Request):
    return {"message": "Welcome to the Email API"}


# TODO: Remove this once out of initial dev
@app.get("/debug")
async def get_debug_info(request: Request):
    headers = request.headers
    form_data = await request.form()

    return {
        "headers": headers,
        "form_data": form_data,
        "settings": settings,
    }


@app.post("/send")
@requires("authenticated")
async def send_email(request: Request):
    headers = request.headers
    subject = headers["X-Mail-Subject"]
    sender_addr = request.user.email
    sender_name = request.user.name

    sender = (f"{sender_name} <{sender_addr}>" if sender_addr else sender_name).strip()

    form_data = await request.form()

    body_lines = [f"{k}: {v}" for k, v in form_data.items()]
    email_body = "\n".join(body_lines)

    email = Email(subject, email_body, settings.from_addr, sender, to={settings.to})

    mailer.send(email)

    return {"email": email}