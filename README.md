# regtech-mail-api

FastAPI-based REST API for sending emails

## Run it

```bash
docker compose up
```

## Development

### Install

```bash
pip install poetry
poetry install
poetry shell
```

### Testing

```bash
pytest
```

## API

### `GET /`

```bash
curl http://localhost:8765
```
```json
{"message":"Welcome to the Email API"}
```

### `POST /send`

```bash
curl -vs -X POST \
-H "X-Mail-Subject: Institution Profile Change" \
-H "X-Mail-Sender-Address: jane.doe@some.org" \
-H "X-Mail-Sender-Name: Jane Doe" \
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
    "sender": "Jane Doe <jane.doe@some.org>",
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

You can browse your emails at:

- http://localhost:8025/

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
