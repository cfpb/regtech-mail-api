# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-mail-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                               |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/regtech\_mail\_api/api.py      |       15 |        0 |        0 |        0 |    100% |           |
| src/regtech\_mail\_api/internal.py |       14 |        0 |        0 |        0 |    100% |           |
| src/regtech\_mail\_api/mailer.py   |       39 |       11 |        8 |        2 |     64% |14, 30-39, 56, 65-66 |
| src/regtech\_mail\_api/models.py   |       21 |        2 |        4 |        2 |     84% |    21, 24 |
| src/regtech\_mail\_api/public.py   |       28 |        1 |        4 |        2 |     91% |23->25, 26 |
| src/regtech\_mail\_api/settings.py |       28 |        0 |        6 |        0 |    100% |           |
|                          **TOTAL** |  **145** |   **14** |   **22** |    **6** | **86%** |           |

1 empty file skipped.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/cfpb/regtech-mail-api/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-mail-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cfpb/regtech-mail-api/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-mail-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcfpb%2Fregtech-mail-api%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-mail-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.