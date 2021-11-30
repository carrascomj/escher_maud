"""Toplevel fixtures."""
import os
import tempfile
from os.path import dirname, join

import pytest


@pytest.fixture
def escher_json_path():
    """Store path to escher map."""
    return join(dirname(__file__), "data", "map_escher_iclau786.json")


@pytest.fixture
def output_maud_dir():
    """Store path to test maud output directory."""
    return join(dirname(__file__), "data", "maud_output_c747bcd761")


@pytest.fixture(scope="function")
def tempfile_html():
    """Make a tempfile location and remove after the test."""
    fd, fname = tempfile.mkstemp(suffix=".html")
    os.close(fd)
    yield fname
    if os.path.exists(fname):
        os.unlink(fname)
