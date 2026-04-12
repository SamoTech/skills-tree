"""Skill: email_sender — send emails via SMTP or SendGrid."""
from __future__ import annotations
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput


class EmailSenderSkill(BaseSkill):
    name = "email_sender"
    description = "Send an email via SMTP. Supports plain text and HTML bodies."
    category = "communication"
    tags = ["email", "smtp", "notification", "outreach"]
    level = "intermediate"
    input_schema = {
        "to": {"type": "string", "required": True, "description": "Recipient email address"},
        "subject": {"type": "string", "required": True},
        "body": {"type": "string", "required": True},
        "html": {"type": "boolean", "default": False},
        "from": {"type": "string", "default": ""},
    }
    output_schema = {
        "sent": {"type": "boolean"},
        "message_id": {"type": "string"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        to = inp.data.get("to", "")
        subject = inp.data.get("subject", "")
        body = inp.data.get("body", "")
        is_html = inp.data.get("html", False)
        from_addr = inp.data.get("from") or os.getenv("SMTP_FROM", "noreply@agentforge.ai")

        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASS", "")

        if not all([to, subject, body]):
            return SkillOutput(success=False, error="to, subject, and body are required")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to
        content_type = "html" if is_html else "plain"
        msg.attach(MIMEText(body, content_type))

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return SkillOutput(success=True, data={"sent": True, "message_id": msg["Message-ID"] or ""})
        except Exception as e:
            return SkillOutput(success=False, error=str(e), data={"sent": False})
