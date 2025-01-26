# Changelog  

## Version 0.2.3  
**Release Date:** September 19, 2023  

### Added  
- Introduced compatibility with Pydantic V2, ensuring seamless integration with the latest versions.  

### Fixed  
- Resolved several bugs related to configuration handling and email validation.  
- Improved overall stability and robustness of the library.  

---

## Version 0.2.2  
**Release Date:** January 14, 2023  

### Updated  
- Enhanced the `setup.py` to streamline installation and dependency management.  
- Revised the README file for better clarity and up-to-date documentation.  

### Fixed  
- Addressed versioning inconsistencies to avoid compatibility issues.  

### Added  
- Full compatibility with Python 3.11.  

---

## Version 0.2.1  
**Release Date:** January 11, 2023  

### Fixed  
- Resolved `aioredis` compatibility issues for Python 3.11.  
- Fixed a critical bug in the `httpx` library dependency.  

---

## Version 0.2.0  
**Release Date:** Febuary 16, 2022  

### Added  
- Introduced `send_mail` and `send_mass_mail` methods, similar to Django or Flask-Mailman.  
- Added extensive docstrings for better API understanding.  
- Expanded the test suite with additional test cases to ensure reliability.  

### Fixed  
- Corrected a significant issue in the `MAIL_START_TLS` and `MAIL_START_SSL` configurations in the `ConnectionConfig` module.  

---

## Version 0.1.1  
**Release Date:** January 19, 2022 

### Added  
- Enabled compatibility with `aioredis > 2.0.0`.  
- Introduced asynchronous support for the `utils.email_check.EmailChecker` class.  

### Fixed  
- Resolved test case issues with the fake Redis client.  
- Corrected typos in the `utils.email_check` file.  

### Updated  
- Updated the `utils.email_check.EmailChecker` class for the latest version of `aioredis`.  
- Refined dependency management to ensure compatibility with new versions.  

---

## Version 0.1.0  
**Release Date:** January 12, 2022  

### Added  
- Included support for template parameters via the `template_params` variable in the `schemas.Message` class.  
- Added module-level docstrings to improve documentation clarity.  
- Documented a future roadmap for feature enhancements.  
- Expanded compatibility to Python 3.10.  
- Enabled users to create custom headers for email attachments.  

### Fixed  
- Resolved issue #20, allowing seamless usage of template parameters.  
- Addressed typos and configuration errors in the `setup.py` file.  
- Fixed broken test cases and improved test coverage.  
- Corrected variable naming issues in the `config.ConnectionConfig` class.  
- Fixed `Literal` import issues for Python 3.6 and 3.7.  

### Updated  
- Revised the `MANIFEST.in` file for better packaging.  
- Updated dependencies to the latest stable versions.  

---

## Older Versions  

### Version 0.0.7  
- Fixed the "long description not found" issue on the PyPI website.  

### Version 0.0.6  
- Enabled access to the `Mail` object via `app.extensions['mailing']`.  

### Version 0.0.5  
- Added a new configuration variable, `MAIL_DEFAULT_SENDER`, with functionality similar to `MAIL_FROM`.  
- Fixed the absence of the `httpx` module in `setup.py`.  
- Renamed `MAIL_SSL` and `MAIL_TLS` to `MAIL_USE_SSL` and `MAIL_USE_TLS`, respectively.  
- Introduced the `add_recipient` and `attach` methods in the `schemas.Message` class.  
- Updated documentation and resolved broken test cases.  

### Version 0.0.4  
- Added setup details to `pyproject.toml` to resolve dependency errors.  

### Version 0.0.2  
- Updated dependencies.  
