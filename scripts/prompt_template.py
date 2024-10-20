from typing import Any
from jinja2 import Environment, FileSystemLoader, select_autoescape # for the prompt templates

def load_template(template_filepath: str, arguments: dict[str, Any]) -> str:
    env = Environment(
        loader=FileSystemLoader(searchpath='../'),
        autoescape=select_autoescape()
    )
    template = env.get_template(template_filepath)
    return template.render(**arguments)