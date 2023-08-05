from pathlib import Path

from jinja2 import Template


class JinjaUtil:
    @staticmethod
    def render_jinja_template(root_file: str | Path, **kvargs) -> str:
        with open(Path(root_file)) as f:
            query_source = f.read()
        query: Template = Template(source=query_source)
        query_string = query.render(**kvargs)
        return query_string
