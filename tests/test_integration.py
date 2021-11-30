"""Test main function, endpoint of the CLI."""

from os.path import dirname, exists, getsize, join, pardir

from click.testing import CliRunner

from escher_maud.vis import main


def test_cli_generates_sized_html(escher_json_path, output_maud_dir, tempfile_html):
    """Test that the CLI endpoint generates an HTML of a size >= the template."""
    runner = CliRunner()
    runner.invoke(main, [output_maud_dir, escher_json_path, tempfile_html])
    assert exists(tempfile_html)
    assert getsize(tempfile_html) >= getsize(
        join(dirname(__file__), pardir, "escher_maud", "templates", "standalone.html")
    )
