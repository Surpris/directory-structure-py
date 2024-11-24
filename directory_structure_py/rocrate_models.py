"""rocrate_models.py

Customized RO-Crate
"""

import importlib.resources
import os
from jinja2 import Template
from rocrate.rocrate import ROCrate as ROCrateOrigin
from rocrate.model import Preview as PreviewOrigin


class Preview(PreviewOrigin):
    """
    Customized RO-Crate preview file

    This object holds a preview of an RO Crate in HTML format_
    """

    def generate_html(self):
        # base_path = os.path.abspath(os.path.dirname(__file__))
        template_str: str = importlib.resources.files(
            __package__
        ).joinpath("templates/preview_template.html.j2").read_text("utf8")
        src: Template = Template(template_str)
        # template_path: str = os.path.join(
        #     base_path, 'templates', 'preview_template.html.j2'
        # )
        # src: Template | None = None
        # with open(template_path, "r", encoding="utf-8") as template:
        #     src = Template(template.read())

        def template_function(func):
            src.globals[func.__name__] = func
            return func

        @template_function
        def stringify(a):
            if type(a) is list:
                return ', '.join(a)
            elif type(a) is str:
                return a
            else:
                if a._jsonld and a._jsonld['name']:
                    return a._jsonld['name']
                else:
                    return a

        @template_function
        def is_object_list(a):
            if type(a) is list:
                for obj in a:
                    if obj is not str:
                        return True
            else:
                return False

        # template.close()
        context_entities = []
        data_entities = []
        for entity in self.crate.contextual_entities:
            context_entities.append(entity._jsonld)
        for entity in self.crate.data_entities:
            data_entities.append(entity._jsonld)
        out_html = src.render(crate=self.crate, context=context_entities, data=data_entities)
        return out_html


class ROCrate(ROCrateOrigin):
    """
    Customized ROCrate class
    """
    def __init__(self, source=None, gen_preview=False, init=False, exclude=None):
        super().__init__(source, gen_preview=False, init=init, exclude=exclude)
        if gen_preview:
            self.add(Preview(self))
