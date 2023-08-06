# from blackline.catalogue.catalogue import Catalogue
# from blackline.store.store import Store
from blackline.models.datastores import DataStore
from blackline.query.template import Template
from jinja2 import Template as JinjaTemplate
from jinja2.runtime import Macro


def test__init__(store: DataStore) -> None:
    # Setup
    adapter = store.adapter

    # Run
    template = Template(adapter=adapter)

    # Assert
    assert isinstance(template, Template)
    assert isinstance(template.env.globals["redact"], Macro)
    assert isinstance(template.env.globals["replace"], Macro)
    assert isinstance(template.env.globals["mask"], Macro)


def test_template_str(store: DataStore) -> None:
    # Setup
    adapter = store.adapter
    template = Template(adapter=adapter)
    expected = """UPDATE {{ table }}\nSET\n{% for column in columns %}\n  {% set value = column.name + "_value" %}\n  {{ redact(cls=column.deidentifier, name=column.name, value=value) -}}\n  {{ replace(cls=column.deidentifier, name=column.name, value=value) -}}\n  {{ mask(cls=column.deidentifier, name=column.name, value=value) -}}\n  {{ "," if not loop.last }}\n{% endfor %}\nWHERE {{ datetime_column }} < :cutoff\n"""  # noqa E501

    # Run
    _template = template.template_str()

    # Assert
    assert _template == expected


def test_template(store: DataStore) -> None:
    # Setup
    adapter = store.adapter
    template = Template(adapter=adapter)

    # Run
    _template = template.template

    # Assert
    assert isinstance(_template, JinjaTemplate)
