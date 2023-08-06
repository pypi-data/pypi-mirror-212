import logging

from blackline.adapters.base import AdapterBase
from blackline.query.templates import deidentifier_marco_base, layout, query
from jinja2 import Environment
from jinja2 import Template as JinjaTemplate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Template(object):
    def __init__(
        self,
        adapter: AdapterBase,
        trim_blocks=True,
        lstrip_blocks=True,
        *args,
        **kwrgs,
    ) -> None:
        self.adapter = adapter
        self.env = Environment(
            *args, trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks, **kwrgs
        )
        self.layout = self.env.from_string(layout)
        self.deidentifier_marco_base = self.env.from_string(deidentifier_marco_base)
        self._load_marcos()

    @property
    def template(self) -> JinjaTemplate:
        return self.env.from_string(self.template_str())

    def _load_marcos(self) -> Environment:
        return self.env.globals.update(
            {
                "redact": self.redact_macro(),
                "replace": self.replace_macro(),
                "mask": self.mask_macro(),
            }
        )

    def _deidentifer_macro(self, name, method) -> str:
        sql_str = self.deidentifier_marco_base.module.deidentifier_marco_base(
            macro_name=name, assignment=getattr(self.adapter, method)()
        )
        logger.debug(f"{name} macro: \n{sql_str}")

        return getattr(self.env.from_string(sql_str).module, name.lower())

    def redact_macro(self) -> str:
        return self._deidentifer_macro(name="Redact", method="redact_template")

    def replace_macro(self) -> str:
        return self._deidentifer_macro(name="Replace", method="replace_template")

    def mask_macro(self) -> str:
        return self._deidentifer_macro(name="Mask", method="mask_template")

    def template_str(self) -> str:
        template = self.env.from_string(query).render(
            layout=self.layout,
            update_statement=self.adapter.update_template(),
            set_statement=self.adapter.set_template(),
            where_statement=self.adapter.where_template(),
        )
        logger.debug(f"render_template:\n{template}")
        return template

    def render_template(self, *args, **kwargs) -> str:
        template = self.template()
        return self.env.from_string(template).render(*args, **kwargs)
