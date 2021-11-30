"""Extend `escher.Builder` with a method that provides a custom tooltip for maud."""

import json
from os.path import expanduser

import escher
from escher.urls import get_url
from escher.util import b64dump
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader("escher_maud", "templates"))


class BuilderMaud(escher.Builder):
    """Extension of `escher.Builder`."""

    def save_maud_html(
        self,
        output_file: str,
        posterior_flux: dict[str, list[float]],
        posterior_conc: dict[str, list[float]],
    ):
        """Save an HTML file containing the map.

        Adapted from `escher.Builder.save_html`.

        Parameters
        ----------
        output_file: str,
            name of the HTML that will be generated.
        posterior_flux: dict[str, list[float]],
            generated with :py:func:`escher_maud.vis.get_flux_posteriors`
        posterior_conc: dict[str, list[float]],
            generated with :py:func:`escher_maud.vis.get_conc_posteriors`

        """
        options = {}
        for key in self.traits(option=True):
            val = getattr(self, key)
            if val is not None:
                options[key] = val
        options_json = json.dumps(options)

        template = env.get_template("standalone.html")
        embedded_css_b64 = (
            b64dump(self.embedded_css) if self.embedded_css is not None else None
        )
        html = template.render(
            escher_url=get_url("escher_min"),
            embedded_css_b64=embedded_css_b64,
            map_data_json_b64=b64dump(self._loaded_map_json),
            model_data_json_b64=b64dump(self._loaded_model_json),
            options_json_b64=b64dump(options_json),
            maud_fluxes_b64=b64dump(posterior_flux),
            maud_concs_b64=b64dump(posterior_conc),
        )

        with open(expanduser(output_file), "wb") as f:
            f.write(html.encode("utf-8"))
