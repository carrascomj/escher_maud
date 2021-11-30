"""Test that the template(s) are valid."""

from os.path import dirname, join, pardir

from jinja2 import Environment


def test_valid_standalone_template(escher_json_path, output_maud_dir, tempfile_html):
    """Test that the CLI endpoint generates an HTML of a size >= the template."""
    env = Environment()
    with open(
        join(
            dirname(__file__),
            pardir,
            "escher_maud",
            "templates",
            "standalone.html",
        )
    ) as template:
        env.parse(template.read())
