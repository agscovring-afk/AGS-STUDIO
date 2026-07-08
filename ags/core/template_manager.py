from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class TemplateManager:


    def __init__(self, path="templates"):

        self.env = Environment(
            loader=FileSystemLoader(path)
        )


    def render(self, template, data):

        tpl = self.env.get_template(template)

        return tpl.render(**data)
