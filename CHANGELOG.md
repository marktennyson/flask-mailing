# Changelog  

## Version 3.0.1
**Release Date:** November 3, 2026  

### 🐛 Bug Fixes
- **Invalid `Content-Transfer-Encoding` on multipart messages** ([#67](https://github.com/marktennyson/flask-mailing/issues/67)):
  the outer `multipart/*` container was given `Content-Transfer-Encoding: base64`
  because the charset was set on the container itself. RFC 2045 §6.4 only allows
  `7bit`, `8bit` or `binary` for multipart entities, and Python's email parser
  reported `InvalidMultipartContentTransferEncodingDefect`. The charset is now
  applied only to individual text parts. Attachments keep their base64 encoding,
  and decoded content is unchanged.
  Reported by [@filak](https://github.com/filak), who also found the cause and suggested the fix. Thank you!

### 🧪 Tests
- Added a regression test that serializes and re-parses a message with HTML and an
  attachment, and checks that it has no MIME defects
  ([#67](https://github.com/marktennyson/flask-mailing/issues/67)).

### 🛠️ Build & CI
- **Docker image build fixed:** the dependency install step ran before `README.md`,
  `LICENSE` and the `flask_mailing/utils` subpackage were copied into the image, so
  `pip install -e .` failed. All files the build needs are now copied first.
- Fixed a new `ruff` lint failure (`PLC0207`) in the test suite.

## Version 3.0.0 🚀 2026-Ready Release
**Release Date:** November 29, 2025  

### 🌟 Future-Proof Architecture
This major release transforms Flask-Mailing into a 2026-ready email solution with cutting-edge Python features, enhanced security, and modern development practices.

### 🔥 Breaking Changes  
- **Minimum Python version raised to 3.10** (modern union syntax support)
- **Minimum Flask version raised to 3.1** (latest Flask with async support)
- **Pydantic v2.11+ required** (latest validation with ConfigDict)
- **Dependencies updated to latest stable versions**
- **Enhanced type safety with stricter validation**
- **Improved async context manager patterns**

### ✨ New Features  
- 🚀 **Python 3.10-3.14 support** with modern union operators (`|`) and built-in generics
- 🛡️ **Advanced security module** with `RateLimiter` and `EmailSecurityValidator`
- ⚡ **Enhanced async/await patterns** with proper context managers
- 🔒 **Improved path traversal protection** and content sanitization
- 📊 **Rate limiting system** to prevent abuse
- 🔐 **Email security validation** with disposable email detection
- 🏗️ **Modern build system** with ruff, mypy, and enhanced tooling

### 📦 Updated Dependencies  
- `aiosmtplib >= 4.0.2` (latest async SMTP client)
- `flask >= 3.1.0` (latest Flask with all security updates)
- `pydantic >= 2.11.0` (modern validation with v2.11 API)
- `pydantic-settings >= 2.9.0` (settings management)
- `email-validator >= 2.3.0` (enhanced email validation)
- `werkzeug >= 3.1.3` (latest WSGI utilities)
- `jinja2 >= 3.1.6` (modern templating)
- `typing-extensions >= 4.13.0` (extended typing support)
- `asgiref >= 3.9.0` (ASGI utilities)
- `blinker >= 1.9.0` (signals support)

### 🛠️ Developer Experience  
- ✅ **Modern pyproject.toml** with ruff, black, isort, mypy configuration
- ✅ **Enhanced CI/CD pipeline** with Python 3.10-3.14 support
- ✅ **Docker containerization** support
- ✅ **Comprehensive security scanning**
- ✅ **Better error messages** with exception chaining
- ✅ **Type safety improvements** throughout codebase

### 🔧 Performance & Reliability
- ⚡ **Connection timeout handling** (30s default)
- 🔄 **Better connection cleanup** in async contexts  
- 📈 **Improved memory usage** with modern Python features
- 🛡️ **Enhanced error recovery** mechanisms

### 📚 Documentation
- Updated all documentation for v3.0.0
- Modern code examples with Flask 3.1+ patterns
- Comprehensive API reference tables
- Installation guide with optional dependencies

## Version 2.1.0
**Release Date:** August 30, 2025  

### 🚀 Major Release - Python 3.13 & Flask 3 Ready
This is a major modernization release that brings Flask-Mailing to 2026 standards.

### Breaking Changes  
- **Minimum Python version raised to 3.9** (was 3.6+)
- **Minimum Flask version raised to 3.0** (was 2.0+)  
- **Updated all dependencies to modern versions**
- **Removed deprecated Python 2/3.6/3.7/3.8 compatibility code**

### Added  
- ✅ **Full Python 3.13 compatibility**
- ✅ **Full Flask 3.x compatibility** 
- ✅ **Modern pyproject.toml configuration**
- ✅ **Type annotations improvements**
- ✅ **Better error handling and validation**
- ✅ **py.typed file for better IDE support**

### Updated  
- 📦 **Dependencies modernized:**
  - `aiosmtplib >= 3.0.0`
  - `flask >= 3.0.0`
  - `pydantic >= 2.0.0`
  - `email-validator >= 2.0.0`
  - `httpx >= 0.25.0`
  - `werkzeug >= 3.0.0`
  - `typing-extensions >= 4.0.0`

### Fixed  
- 🐛 **Pydantic v2 compatibility** - Fixed deprecated `Config` class usage
- 🐛 **Type annotation improvements** - Better type safety
- 🐛 **Email validation modernized** - Uses latest email-validator
- 🐛 **Async/await patterns improved** - Better async support
- 🐛 **Import error handling** - Graceful dependency handling

### Deprecated  
- ⚠️ **Python < 3.9 support removed**
- ⚠️ **Flask < 3.0 support removed**

### Development & Testing  
- 🧪 **Test suite updated for modern pytest**
- 🧪 **Tox configuration updated for Python 3.9-3.13**
- 🧪 **CI/CD ready for modern Python versions**

### Migration Guide  
To upgrade to v3.0.0:
1. **Upgrade Python to 3.9+** (recommended: 3.11+ for best performance)
2. **Upgrade Flask to 3.0+**
3. **Update your requirements.txt** with new minimum versions
4. **Test your application** - most APIs remain the same

---

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
