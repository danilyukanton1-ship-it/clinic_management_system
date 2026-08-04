from datetime import UTC, datetime

from infrastructure.celery import celery_app, run
from infrastructure.notifications.smtp import SMTPEmailService
from infrastructure.notifications.template_renderer import TemplateRenderer


@celery_app.task
def send_verify_email(
    email: str,
    username: str,
    verification_code: str,
):
    renderer = TemplateRenderer()
    email_service = SMTPEmailService()

    html = renderer.render(
        "verification.html",
        username=username,
        code=verification_code,
        minutes=10,
        year=datetime.now(UTC).year,
    )
    run(
        email_service.send(
            email_receiver=email,
            subject="Verify your email",
            body=f"Your verification code is {verification_code}",
            html=html,
        )
    )


@celery_app.task
def send_success_password_reset_email(
    email: str,
    username: str,
    changed_at: datetime,
):
    renderer = TemplateRenderer()
    email_service = SMTPEmailService()

    html = renderer.render(
        "password_change.html",
        username=username,
        changed_at=changed_at,
        year=datetime.now(UTC).year,
    )
    run(
        email_service.send(
            email_receiver=email,
            subject="Password Changed",
            body="Your password has been changed!",
            html=html,
        )
    )
