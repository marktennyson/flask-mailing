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