from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from regtech_mail_api.settings import kc_settings
from regtech_mail_api.public import router as public_router
from regtech_mail_api.internal import router as internal_router

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
    allow_headers=["*"],
)

app.include_router(internal_router, prefix="/internal")
app.include_router(public_router, prefix="/public")
