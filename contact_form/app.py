#!/usr/bin/env python3
"""
Contact form handler for Rose Medical Pavilion.
Runs as a Flask app on port 5001, proxied by nginx at /contact.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://rosemedicalpavilion.com", "https://sandbox.rosemedicalpavilion.com"])

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]
TO_EMAIL  = "info@rosemedicalpavilion.com"
FROM_EMAIL = "benjamin@rosemedicalpavilion.com"


def send_email(name, email, phone, message):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New Contact Form Submission — {name}"
    msg["From"]    = FROM_EMAIL
    msg["To"]      = TO_EMAIL
    msg["Reply-To"] = email

    body = f"""\
New contact form submission from rosemedicalpavilion.com

Name:    {name}
Email:   {email}
Phone:   {phone or 'Not provided'}

Message:
{message}
"""
    html = f"""\
<html><body>
<h2>New Contact Form Submission</h2>
<table>
  <tr><td><strong>Name</strong></td><td>{name}</td></tr>
  <tr><td><strong>Email</strong></td><td><a href="mailto:{email}">{email}</a></td></tr>
  <tr><td><strong>Phone</strong></td><td>{phone or 'Not provided'}</td></tr>
</table>
<h3>Message</h3>
<p>{message.replace(chr(10), '<br>')}</p>
</body></html>
"""
    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

    # Confirmation email to submitter
    confirm = MIMEMultipart("alternative")
    confirm["Subject"] = "We received your message — Rose Medical Pavilion"
    confirm["From"]    = FROM_EMAIL
    confirm["To"]      = email

    confirm_text = f"""\
Hi {name},

Thank you for reaching out to Rose Medical Pavilion. We received your message and will be in touch within one business day.

If you need immediate assistance, please call us at (602) 892-7467.

— Rose Medical Pavilion
22044 N 44th St, Suite 200, Phoenix, AZ 85050
"""
    confirm_html = f"""\
<html><body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto;">
<div style="background:#005da8;padding:24px 32px;">
  <h2 style="color:#fff;margin:0;">Rose Medical Pavilion</h2>
</div>
<div style="padding:32px;">
  <p>Hi {name},</p>
  <p>Thank you for reaching out to Rose Medical Pavilion. We received your message and will be in touch within one business day.</p>
  <p>If you need immediate assistance, please call us at <a href="tel:+16028927467" style="color:#005da8;">(602) 892-7467</a>.</p>
  <hr style="border:none;border-top:1px solid #eee;margin:24px 0;">
  <p style="font-size:13px;color:#888;">Rose Medical Pavilion &nbsp;|&nbsp; 22044 N 44th St, Suite 200, Phoenix, AZ 85050</p>
</div>
</body></html>
"""
    confirm.attach(MIMEText(confirm_text, "plain"))
    confirm.attach(MIMEText(confirm_html, "html"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, email, confirm.as_string())


@app.route("/contact", methods=["POST"])
def contact():
    # Honeypot — bots fill this field, humans don't
    if request.form.get("website"):
        return redirect("/?success=1")

    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    phone   = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        if request.is_json:
            return jsonify({"error": "Name, email, and message are required."}), 400
        return redirect("/contact-us/?error=missing")

    try:
        send_email(name, email, phone, message)
    except Exception as e:
        app.logger.error(f"Email send failed: {e}")
        if request.is_json:
            return jsonify({"error": "Failed to send message. Please call us directly."}), 500
        return redirect("/contact-us/?error=send")

    if request.is_json:
        return jsonify({"success": True})
    return redirect("/contact-us/?success=1")


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
