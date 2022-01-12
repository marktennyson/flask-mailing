## 0.0.2 
- Update dependencies

## 0.0.4
- added setup details to pyproject.toml file to solve the dependency error.

## 0.0.5
- Added one more config variable named `MAIL_DEFAULT_SENDER`. It's as same as `MAIL_FROM` config var.
- Fixed absent of `httpx` module at the __setup.py__ file.
- Config var `MAIL_SSL` and `MAIL_TLS` changes to `MAIL_USE_SSL` and `MAIL_USE_TLS` accordingly.
- added `add_recipient` and `attach` method to the __schemas.Message__ class.
- Fixed some broken test cases.
- modifications at the documentation.

## 0.0.6
- Now the user can access the `Mail` object from the app extension dictionary: `app.extension['mailing']`

## 0.0.7
- Solved the `long description not found` on the PYPI website.

## 0.1.0 [Upcoming]
- Fixed issue #20 
- Now the user can pass template parameters by using `template_params` variable on the `schemas.Message` class.
- Dependencies update.
- Added `future roadmap` on the docs.
- Major typo fixed at setup.py
- Updated the `MANIFEST.in` file.
- Python version 3.10.0 compatibility. 
- Fixed some broken test cases.
- Added some more test cases.
- Fixed the Variable name issue at `config.ConnectionConfig` class.
- Now the users are allowed to create custom headers for attachments.
- Fixed Literal import for Python 3.6 and 3.7