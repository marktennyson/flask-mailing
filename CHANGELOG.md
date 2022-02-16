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
- `Fixed` the `long description not found` on the PYPI website.

## 0.1.0
- `Fixed` issue #20 . Now the user can pass template parameters by using `template_params` variable on the `schemas.Message` class.
- `Fixed` major typo at setup.py
- `Fixed` some broken test cases.
- `Fixed` the Variable name issue at `config.ConnectionConfig` class.
- `Fixed` Literal import for Python 3.6 and 3.7

- `Added` module docstring.
- `Added` `future roadmap` on the docs.
- `Added` some more test cases.
- `Added` the compatibility for Python 3.10
- `Added` the feature to allow users to create custom headers for attachments.

- `Updated` the `MANIFEST.in` file.
- `Updated` the required dependencies.

## 0.1.1
- `Fixed` broken test cases for fake redis client.
- `Fixed` some typo at `utils.email_check` file.
- `Added` `aioredis > 2.0.0` compatibility.
- `Added` fully asynchronous support for `utils.email_check.EmailChecker` class.
- `Updated` the `utils.email_check.EmailChecker` class for the new version of `aioredis`.
- `Updated` the required dependencies.

## 0.2.0[Upcoming]
- `Added` `send_mail`, `send_mass_mail` methods very similar to `Django` or `Flask-Mailman`.
- `Added` more docstring for better understanding of all the apis.
- `Fixed` several typos.
- `Fixed` major bug at `MAIL_START_TLS`/`MAIL_START_SSL` configuration at `ConnectionConfig`.