layout = """{% block table required %}
{% endblock %}
{% block set_columns required %}
{% endblock %}
{% block cond required %}
{% endblock %}
"""

query = """{% extends layout %}
{% block table %}
{{ update_statement }}
{% endblock %}
{% block set_columns %}
{{ set_statement }}
{% raw -%}
{% for column in columns %}
  {% set value = column.name + "_value" %}
  {{ redact(cls=column.deidentifier, name=column.name, value=value) -}}
  {{ replace(cls=column.deidentifier, name=column.name, value=value) -}}
  {{ mask(cls=column.deidentifier, name=column.name, value=value) -}}
  {{ "," if not loop.last }}
{% endfor %}
{% endraw %}
{% endblock %}
{% block cond %}
{{ where_statement }}
{% endblock %}
"""

deidentifier_marco_base = """{% macro deidentifier_marco_base(macro_name, assignment) -%}
{{'{% macro '}}{{macro_name | lower}}{{'(cls, name, value) -%}' }}
{{'{% if cls.__class__.__name__ == "'}}{{ macro_name }}{{'"%}'}}{{assignment}}{{'{% endif %}'}}
{{'{%- endmacro %}'}}
{%- endmacro %}
"""
