"""rocrate_models.py

Customized RO-Crate
"""

import copy
import importlib.resources
import json
import os
from pathlib import Path
from typing import Dict
from jinja2 import Template
from rocrate.model import (
    Metadata as MetadataOrigin,
    Preview as PreviewOrigin
)
from directory_structure_py.constants import ENSURE_ASCII


class Metadata(MetadataOrigin):
    """
    Customized RO-Crate metadata file.
    """
    BASENAME = "ro-crate-metadata.json"
    PROFILE = "https://w3id.org/ro/crate/1.1"

    def __init__(self, crate, source=None, dest_path=None, properties=None):
        if source is None and dest_path is None:
            dest_path = self.BASENAME
        super().__init__(
            crate,
            source=source,
            dest_path=dest_path,
            properties=properties
        )

    def write(self, base_path):
        write_path = Path(base_path) / self.id
        as_jsonld = self.generate()
        with open(write_path, 'w', encoding="utf-8") as outfile:
            json.dump(
                as_jsonld, outfile, indent=4, sort_keys=True, ensure_ascii=ENSURE_ASCII
            )


class Preview(PreviewOrigin):
    """
    Customized RO-Crate preview file.

    This object holds a preview of an RO Crate in HTML format_
    """

    def generate_html(self, template_path: str = None):
        if isinstance(template_path, str) and os.path.isfile(template_path):
            with open(template_path, "r", encoding="utf-8") as ff:
                template_str = ff.read()
        else:
            template_str: str = importlib.resources.files(
                __package__
            ).joinpath("templates/preview_template.html.j2").read_text("utf8")
        src: Template = Template(template_str)

        def template_function(func):
            src.globals[func.__name__] = func
            return func

        @template_function
        def stringify(a):
            if isinstance(a, list):
                return ', '.join(a)
            if isinstance(a, str):
                return a
            if a.as_jsonld() and a.as_jsonld()['name']:
                return a.as_jsonld()['name']
            return a

        @template_function
        def is_object_list(a):
            if isinstance(a, list):
                for obj in a:
                    if not isinstance(obj, str):
                        return True
            return False

        @template_function
        def is_object_dict(a):
            if isinstance(a, Dict):
                return True
            return False

        context_entities = []
        data_entities = []
        for entity in self.crate.contextual_entities:
            context_entities.append(entity.as_jsonld())
        for entity in self.crate.data_entities:
            entity_: Dict = copy.deepcopy(entity.as_jsonld())
            for k, v in entity_.items():
                if not isinstance(v, str):
                    continue
                v_ = v.replace("'", "\"")
                try:
                    v_ = json.loads(v_)
                    if isinstance(v_, Dict):
                        entity_[k] = v_
                except TypeError:
                    continue
                except json.JSONDecodeError:
                    continue
            # data_entities.append(entity.as_jsonld())
            data_entities.append(entity_)
        out_html = src.render(
            crate=self.crate, context=context_entities, data=data_entities)
        return out_html

    def write(self, dest_base, template_path: str = None):
        if self.source:
            super().write(dest_base)
        else:
            write_path = Path(dest_base) / self.id
            out_html = self.generate_html(template_path)
            with open(write_path, 'w', encoding="utf-8") as outfile:
                outfile.write(out_html)
