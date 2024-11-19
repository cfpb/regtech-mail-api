from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from regtech_mail_api.models import Email
from regtech_mail_api.settings import kc_settings, EmailApiSettings
from regtech_mail_api.mailer import create_mailer

from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware

from regtech_api_commons.api.router_wrapper import Router
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
    allow_headers=["*"],
)

settings = EmailApiSettings()

router = Router()


@router.get("/welcome")
@requires("authenticated")
def read_root(request: Request):
    return {"message": "Welcome to the Email API"}


@router.post("/send")
@requires("authenticated")
async def send_email(request: Request):
    sender_addr = request.user.email
    sender_name = request.user.name if request.user.name else ""
    type = request.headers["case-type"]

    header = "[BETA]"
    if "cfpb" in sender_addr.lower().split("@")[-1]:
        header = "[CFPB BETA]"
    if settings.environment:
        header = f"[{settings.environment}]"

    subject = f"{header} SBL User Request for {type}"

    form_data = await request.form()

    body_lines = [f"{k}: {v}" for k, v in form_data.items()]
    email_body = f"Contact Email: {sender_addr}\n"
    email_body += f"Contact Name: {sender_name}\n\n"
    email_body += "\n".join(body_lines)

    email = Email(subject, email_body, settings.from_addr, to={settings.to})

    create_mailer().send(email)

    return {"email": email}


app.include_router(router)
