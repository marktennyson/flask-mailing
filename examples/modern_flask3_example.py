#!/usr/bin/env python3
"""
Flask-Mailing v3.0.0 - 2026-Ready Example for Python 3.10+ and Flask 3.1+

This example demonstrates the fully modernized Flask-Mailing library
with latest Flask 3.1+, Python 3.10-3.14, and Pydantic v2.11+ compatibility.
Features modern type hints, async patterns, and enhanced security.
"""

from __future__ import annotations

from flask import Flask, jsonify, request
from flask_mailing import Mail, Message


def create_app() -> Flask:
    """Application factory pattern for Flask 3.1+"""
    app = Flask(__name__)

    # Modern Flask-Mailing configuration for 2026
    app.config.update(
        MAIL_USERNAME="your.email@example.com",
        MAIL_PASSWORD="your_app_password",
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        MAIL_DEFAULT_SENDER="your.email@example.com",
        MAIL_FROM_NAME="Flask-Mailing v3.0.0 - 2026 Ready",
    )

    # Initialize mail with Flask 3.1+
    mail = Mail(app)

    @app.route("/")
    def index():
        return jsonify(
            {
                "message": "Flask-Mailing v3.0.0 - 2026 Ready with Python 3.10+ & Flask 3.1+!",
                "version": "3.0.0",
                "python_version": "3.10-3.14",
                "flask_version": "3.1+",
                "pydantic_version": "2.11+",
                "features": [
                    "Modern Python 3.10+ union type hints (|)",
                    "Built-in generic types (list, dict)",
                    "Async/await context managers",
                    "Pydantic v2.11+ field validators",
                    "Enhanced security and validation",
                    "Better error handling with proper chaining",
                    "Performance optimizations",
                    "Python 3.14 ready architecture",
                ],
            }
        )

    @app.route("/send-simple", methods=["POST"])
    async def send_simple_email():
        """Send a simple email using the modern async pattern"""
        try:
            data = request.get_json() or {}
            recipient = data.get("to", "test@example.com")
            subject = data.get("subject", "Flask-Mailing v3.0.0 Test")

            message = Message(
                subject=subject,
                recipients=[recipient],
                body="Hello from Flask-Mailing v3.0.0! 🚀\n\nThis email was sent using the modernized Flask-Mailing library with Python 3.10-3.14 and Flask 3.x support.",
                subtype="plain",
            )

            await mail.send_message(message)

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": f"Email sent successfully to {recipient}",
                        "version": "3.0.0",
                    }
                ),
                200,
            )

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/send-html", methods=["POST"])
    async def send_html_email():
        """Send HTML email with modern async/await"""
        try:
            data = request.get_json() or {}
            recipient = data.get("to", "test@example.com")

            html_content = """
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">🚀 Flask-Mailing v3.0.0</h1>
                        <p>Congratulations! You're using the modernized Flask-Mailing library.</p>
                        
                        <h2 style="color: #34495e;">New Features in v3.0.0:</h2>
                        <ul>
                            <li>✅ Python 3.10-3.14 compatibility</li>
                            <li>✅ Flask 3.1+ support</li>
                            <li>✅ Modern async/await patterns</li>
                            <li>✅ Pydantic v2.11+ integration</li>
                            <li>✅ Enhanced type safety</li>
                            <li>✅ Better error handling</li>
                        </ul>
                        
                        <p style="background: #ecf0f1; padding: 15px; border-radius: 5px;">
                            <strong>Note:</strong> This library is now fully compatible with Python 3.10+ 
                            and provides excellent performance with Python 3.14.
                        </p>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #7f8c8d; font-size: 14px;">
                            Sent with ❤️ using Flask-Mailing v3.0.0
                        </p>
                    </div>
                </body>
            </html>
            """

            message = Message(
                subject="🚀 Flask-Mailing v3.0.0 - HTML Email Test",
                recipients=[recipient],
                html=html_content,
                subtype="html",
            )

            await mail.send_message(message)

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": f"HTML email sent successfully to {recipient}",
                        "version": "3.0.0",
                    }
                ),
                200,
            )

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/send-bulk", methods=["POST"])
    async def send_bulk_emails():
        """Send bulk emails using modern async patterns"""
        try:
            data = request.get_json() or {}
            recipients = data.get(
                "recipients", ["test1@example.com", "test2@example.com"]
            )

            # Prepare email data tuples for bulk sending
            email_data = []
            for recipient in recipients:
                email_data.append(
                    (
                        "Flask-Mailing v3.0.0 - Bulk Email",
                        f"Hello!\n\nThis is a bulk email sent to {recipient} using Flask-Mailing v3.0.0",
                        [recipient],
                    )
                )

            # Send bulk emails
            await mail.send_mass_mail(tuple(email_data))

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": f"Bulk emails sent to {len(recipients)} recipients",
                        "recipients": recipients,
                        "version": "3.0.0",
                    }
                ),
                200,
            )

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()

    print("🚀 Flask-Mailing v3.0.0 - Modern Example")
    print("=" * 50)
    print("✅ Python 3.10-3.14 compatible")
    print("✅ Flask 3.1+ ready")
    print("✅ Modern async/await support")
    print("✅ Type-safe with Pydantic v2.11+")
    print()
    print("Available endpoints:")
    print("  GET  /                  - Info about v3.0.0")
    print("  POST /send-simple       - Send simple email")
    print("  POST /send-html         - Send HTML email")
    print("  POST /send-bulk         - Send bulk emails")
    print()
    print("Example usage:")
    print("  curl -X POST http://127.0.0.1:5000/send-simple \\")
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"to": "your@email.com", "subject": "Test v3.0.0"}\'')
    print()

    # For development - in production use proper ASGI server
    app.run(debug=True, host="127.0.0.1", port=5000)
