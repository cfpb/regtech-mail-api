# regtech-mail-api

FastAPI-based REST API for sending emails

## Run it

The regtech-mail-api has been incorporated into the SBL Project docker-compose.  See the SBL Project [LOCAL_DEV_COMPOSE](https://github.com/cfpb/sbl-project/blob/main/LOCAL_DEV_COMPOSE.md) for instructions on running the services.

## Development

### Install

```bash
pip install poetry
poetry install
poetry shell
```

### Testing

```bash
pytest (from within a poetry shell)
```
or

```bash
poetry run pytest
```

## API
The API endpoints require authentication to access.  The service uses the [regtech-api-commons](https://github.com/cfpb/regtech-api-commons) library to utilize OAuth2 authentication, currently using Keycloak.
To use either endpoint, you must first get an access token from Keycloak. The Contact Name and Email, derived from the Access Token, will be put into the body of the email.

To get an access token, run the following curl command, using the Keycloak user you wish to test with (see [LOCAL_DEV_COMPOSE](https://github.com/cfpb/sbl-project/blob/main/LOCAL_DEV_COMPOSE.md) for launching Keycloak):

```
export RT_ACCESS_TOKEN=$(curl 'localhost:8880/realms/regtech/protocol/openid-connect/token' \
-X POST \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=<user>' \
--data-urlencode 'password=<pass>' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'client_id=regtech-client' | jq -r '.access_token')
```

### `GET /`

```bash
curl -H "Authorization: Bearer ${RT_ACCESS_TOKEN}" http://localhost:8765
```
```json
{"message":"Welcome to the Email API"}
```

### `POST /send`

```bash
curl -vs -X POST \
-H "Authorization: Bearer ${RT_ACCESS_TOKEN}" \
-H "X-Mail-Subject: Institution Profile Change" \
-F lei=1234567890ABCDEFGHIJ \
-F "institution_name_1=Fintech 1" \
-F tin_1=12-3456789 \
-F rssd_1=1234567 \
http://localhost:8765/send | jq '.'
```
```json
{
  "email": {
    "subject": "Institution Profile Change",
    "body": "lei: 1234567890ABCDEFGHIJ\ninstitution_name_1: Fintech 1\ntin_1: 12-3456789\nrssd_1: 1234567",
    "from_addr": "noreply@localhost.localdomain",
    "to": [
      "cases@localhost.localdomain"
    ],
    "cc": null,
    "bcc": null
  }
}
```

## Mailpit

The developer setup uses [Mailpit](https://mailpit.axllent.org/) as a mock
SMTP server. The Mail API is pre-configured to point at Mailpit's SMTP port.
Mailpit also includes a web interface for viewing email messages.

Mailpit has been included in the SBL Project docker-compose.  See the SBL Project [LOCAL_DEV_COMPOSE](https://github.com/cfpb/sbl-project/blob/main/LOCAL_DEV_COMPOSE.md).

You can browse your emails at:

- http://localhost:8025/


## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
