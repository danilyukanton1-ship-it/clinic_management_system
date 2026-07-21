from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateRenderer:

    def __init__(self) -> None:
        template_dir = Path(__file__).parent.parent / "templates"

        self._env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
        )

    def render(self, template_name: str, **context) -> str:
        return self._env.get_template(template_name).render(**context)

