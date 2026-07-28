from infrastructure.notifications.smtp import SMTPEmailService
from infrastructure.notifications.template_renderer import TemplateRenderer


def get_smtp_service():
    return SMTPEmailService()


def get_template_renderer():
    return TemplateRenderer()
