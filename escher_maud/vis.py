"""Data processing from infd to escher visualization."""
from os.path import join

import arviz as az
import click
import escher

from .builder_ext import BuilderMaud


def setup_map(
    map_path: str,
    color_none: str = "#DDDDDD",
) -> escher.Builder:
    """Set a `escher.Builder` and turn everything to gray."""
    escher_map = BuilderMaud(map_json=str(map_path))
    escher_map.reaction_no_data_color = color_none
    escher_map.metabolite_no_data_color = color_none
    # reactions with data are highlighted
    escher_map.reaction_scale = [
        {"type": "min", "color": "#C1D5F7", "size": 12},
        {"type": "median", "color": "#8195d7", "size": 20},
        {"type": "max", "color": "#4175d7", "size": 25},
    ]
    escher_map.metabolite_scale = [
        {"type": "min", "color": "#fedebe", "size": 12},
        {"type": "median", "color": "#ffaf42", "size": 20},
        {"type": "max", "color": "#fd5602", "size": 25},
    ]
    escher_map.enable_tooltips = ["label"]
    return escher_map


def get_summary_data(
    infd: az.InferenceData,
) -> tuple[dict[str, float], dict[str, float]]:
    """Retrive the means of the flux and concentrations over the chains."""
    reac_xa = infd.posterior["flux"]
    met_xa = infd.posterior["conc"]
    flux_reacs = {
        # (chain, draw, experiment, reaction)
        reac: reac_xa.data[:, :, 0, i].mean()
        for i, reac in enumerate(reac_xa.coords["reactions"].data)
    }
    conc_mets = {
        met: met_xa.data[:, :, 0, i].mean()
        for i, met in enumerate(met_xa.coords["mics"].data)
    }
    return flux_reacs, conc_mets


def get_flux_posteriors(
    infd: az.InferenceData,
) -> dict[str, list[float]]:
    """Retrieve flux posterior distributions over the chains."""
    reac_xa = infd.posterior["flux"]
    # TODO: handle chains
    flux_reacs = {
        # (chain, draw, experiment, reaction)
        reac: {
            exp: reac_xa.data[:, :, j, i].flatten().tolist()
            for j, exp in enumerate(reac_xa.experiments.data)
        }
        for i, reac in enumerate(reac_xa.coords["reactions"].data)
    }
    return flux_reacs


def get_conc_posteriors(
    infd: az.InferenceData,
) -> dict[str, list[float]]:
    """Retrieve concentration posterior distrutions over the chains."""
    met_xa = infd.posterior["conc"]
    # TODO: handle chains
    conc_mets = {
        met: {
            exp: met_xa.data[:, :, j, i].flatten().tolist()
            for j, exp in enumerate(met_xa.experiments.data)
        }
        for i, met in enumerate(met_xa.coords["mics"].data)
    }
    return conc_mets


@click.command()
@click.argument(
    "output_maud",
    type=click.Path(exists=True, dir_okay=True),
)
@click.argument(
    "escher_json",
    type=click.Path(exists=True, dir_okay=False),
)
@click.argument(
    "output_html",
    type=click.Path(dir_okay=False),
)
def main(
    output_maud: click.Path,
    escher_json: click.Path,
    output_html: click.Path,
):
    """Generate standalone escher map with maud posteriors in the tooltip.

    Parameters
    ----------
    output_maud: click.Path
        path to a maud output directory generated with `maud sample`
    escher_json: click.Path
        path to a JSON escher map
    output_html: click.Path
        name of the HTML that will be generated

    Example
    -------

    .. code-block:: shell

       git clone https://github.com/carrascomj/escher_maud.git
       cd escher_maud/tests/data
       escher_maud map_escher_iclau786.json maud_output_c747bcd761 index.html

    """
    infd = az.from_netcdf(join(output_maud, "infd.nc"))
    flux_reacs, conc_mets = get_summary_data(infd)
    escher_map = setup_map(escher_json)
    escher_map.reaction_data = flux_reacs
    escher_map.metabolite_data = conc_mets
    posterior_flux = get_flux_posteriors(infd)
    posterior_conc = get_conc_posteriors(infd)
    escher_map.save_maud_html(output_html, posterior_flux, posterior_conc)


if __name__ == "__main__":
    main()
