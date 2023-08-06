#!/usr/bin/env python

# stdlib imports
import pathlib

import numpy as np

# third party imports
import validate
from configobj import ConfigObj

# local imports
from strec.config import get_select_config
from strec.sm_probs import get_probs
from strec.subtype import SubductionSelector, get_event_details


def assert_probs_equal(prob1, prob2):
    for key, value1 in prob1.items():
        value2 = prob2[key]
    np.testing.assert_allclose(value1, value2)


EVENT_DETAILS = {
    "nc73855896": {
        "latitude": 36.2081667,
        "longitude": -119.6201667,
        "depth": 22.04,
        "magnitude": 2.48,
    },
    "ak0219neiszm": {
        "latitude": 55.3635,
        "longitude": -157.8876,
        "depth": 35,
        "magnitude": 8.2,
        "tensor": {
            "type": "Mww",
            "source": "us",
            "mrr": 1.1306e21,
            "mtt": -7.862e20,
            "mpp": -3.444e20,
            "mrt": 1.6711e21,
            "mrp": 1.2237e21,
            "mtp": -5.231e20,
            "T": {"azimuth": 323.0, "plunge": 59.0},
            "N": {"azimuth": 54.0, "plunge": 1.0},
            "P": {"azimuth": 145.0, "plunge": 31.0},
            "NP1": {"rake": 94.53, "strike": 238.78, "dip": 14.36},
            "NP2": {"rake": 88.84, "strike": 54.11, "dip": 75.68},
        },
    },
    "us6000k0xf": {
        "latitude": -35.6626,
        "longitude": -73.5404,
        "depth": 11.586,
        "magnitude": 6.3,
        "tensor": {
            "type": "Mww",
            "source": "us",
            "mrr": 2.0787e18,
            "mtt": 5.43e16,
            "mpp": -2.133e18,
            "mrt": -8.914e17,
            "mrp": -2.8441e18,
            "mtp": -5.619e17,
            "T": {"azimuth": 110.0, "plunge": 63.0},
            "N": {"azimuth": 16.0, "plunge": 2.0},
            "P": {"azimuth": 285.0, "plunge": 27.0},
            "NP1": {"rake": 83.39, "strike": 9.81, "dip": 18.15},
            "NP2": {"rake": 92.16, "strike": 196.76, "dip": 71.97},
        },
    },
    "us7000jhwi": {
        "latitude": 38.4074,
        "longitude": -96.8283,
        "depth": 5,
        "magnitude": 2.6,
    },
    "hv73350092": {
        "latitude": 18.8155,
        "longitude": -155.160333333333,
        "depth": 7.79,
        "magnitude": 4.12,
    },
    "ak0156uj8rk3": {
        "latitude": 56.594,
        "longitude": -156.4301,
        "depth": 72.6,
        "magnitude": 6.8,
        "tensor": {
            "type": "Mww",
            "source": "us",
            "mrr": 4.54e18,
            "mtt": -3.51e18,
            "mpp": -1.03e18,
            "mrt": 8.33e18,
            "mrp": 1.021e19,
            "mtp": 1.263e19,
            "T": {"azimuth": 311.0, "plunge": 39.0},
            "N": {"azimuth": 138.0, "plunge": 51.0},
            "P": {"azimuth": 44.0, "plunge": 3.0},
            "NP1": {"rake": 148.0, "strike": 351.0, "dip": 66.0},
            "NP2": {"rake": 27.0, "strike": 95.0, "dip": 61.0},
        },
    },
    "us6000b9r9": {
        "latitude": 54.5622,
        "longitude": -161.0906,
        "depth": 6.6,
        "magnitude": 5.1,
        "tensor": {
            "type": "Mww",
            "source": "us",
            "mrr": -1.6366e16,
            "mtt": 5.1257e16,
            "mpp": -3.4891e16,
            "mrt": -1.3335e16,
            "mrp": 3.1425e16,
            "mtp": -3.1544e16,
            "T": {"azimuth": 202.0, "plunge": 16.0},
            "N": {"azimuth": 314.0, "plunge": 53.0},
            "P": {"azimuth": 102.0, "plunge": 32.0},
            "NP1": {"rake": -167.32, "strike": 245.99, "dip": 55.35},
            "NP2": {"rake": -35.31, "strike": 148.7, "dip": 79.59},
        },
    },
    "nc1091110": {
        "latitude": 36.0758333,
        "longitude": -120.0185,
        "depth": 65.556,
        "magnitude": 3.24,
    },
}

EVENT_PROBS = {
    "nc73855896": {
        "acr": 1.0,
        "scr": 0.0,
        "subduction": 0.0,
        "volcanic": 0.0,
        "acr_shallow": 1.0,
        "acr_deep": 0.0,
        "scr_shallow": 0.0,
        "subduction_crustal": 0.0,
        "subduction_interface": 0.0,
        "subduction_intraslab": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.0,
        "interface": 0.0,
        "intraslab": 0.0,
    },
    "ak0219neiszm": {
        "acr": 0.0,
        "scr": 0.0,
        "subduction": 1.0,
        "volcanic": 0.0,
        "acr_shallow": 0.0,
        "acr_deep": 0.0,
        "scr_shallow": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.0,
        "interface": 1.0,
        "intraslab": 0.0,
    },
    "us6000k0xf": {
        "acr": 0.3981659709138359,
        "scr": 0.0,
        "subduction": 0.6018340290861641,
        "volcanic": 0.0,
        "acr_shallow": 0.3981659709138359,
        "acr_deep": 0.0,
        "scr_shallow": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.0,
        "interface": 0.6018340290861641,
        "intraslab": 0.0,
    },
    "us7000jhwi": {
        "acr": 0.0,
        "scr": 1.0,
        "subduction": 0.0,
        "volcanic": 0.0,
        "acr_shallow": 0.0,
        "acr_deep": 0.0,
        "scr_shallow": 1.0,
        "subduction_crustal": 0.0,
        "subduction_interface": 0.0,
        "subduction_intraslab": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.0,
        "interface": 0.0,
        "intraslab": 0.0,
    },
    "hv73350092": {
        "acr": 0.0,
        "scr": 0.0,
        "subduction": 0.0,
        "volcanic": 1.0,
        "acr_shallow": 0.0,
        "acr_deep": 0.0,
        "scr_shallow": 0.0,
        "subduction_crustal": 0.0,
        "subduction_interface": 0.0,
        "subduction_intraslab": 0.0,
        "volcanic_shallow": 1.0,
        "crustal": 0.0,
        "interface": 0.0,
        "intraslab": 0.0,
    },
    "ak0156uj8rk3": {
        "acr": 0.0,
        "scr": 0.0,
        "subduction": 1.0,
        "volcanic": 0.0,
        "acr_shallow": 0.0,
        "acr_deep": 0.0,
        "scr_shallow": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.0,
        "interface": 0.0,
        "intraslab": 1.0,
    },
    "us6000b9r9": {
        "acr": 0.0,
        "scr": 0.0,
        "subduction": 1.0,
        "volcanic": 0.0,
        "acr_shallow": 0.0,
        "acr_deep": 0.0,
        "scr_shallow": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.75,
        "interface": 0.25,
        "intraslab": 0.0,
    },
    "nc1091110": {
        "acr": 1.0,
        "scr": 0.0,
        "subduction": 0.0,
        "volcanic": 0.0,
        "acr_shallow": 0.0,
        "acr_deep": 1.0,
        "scr_shallow": 0.0,
        "subduction_crustal": 0.0,
        "subduction_interface": 0.0,
        "subduction_intraslab": 0.0,
        "volcanic_shallow": 0.0,
        "crustal": 0.0,
        "interface": 0.0,
        "intraslab": 0.0,
    },
}


def test_get_region_probs():
    data_dir = (
        pathlib.Path(__file__).parent / ".." / ".." / ".." / "src" / "strec" / "data"
    )
    select_conf = data_dir / "select.conf"
    config, _ = get_select_config(select_conf)
    selector = SubductionSelector(verbose=False, prefix="")

    # loop over test event details and probabilities
    for eventid, details in EVENT_DETAILS.items():
        print(f"Testing event {eventid}")
        tensor = None
        if "tensor" in details:
            tensor = details["tensor"]
        strec_info = selector.getSubductionType(
            details["latitude"],
            details["longitude"],
            details["depth"],
            details["magnitude"],
            eventid=eventid,
            tensor_params=tensor,
        )
        probs = get_probs(details["magnitude"], details["depth"], strec_info, config)
        cmp_probs = EVENT_PROBS[eventid]
        assert_probs_equal(probs, cmp_probs)


def test_get_config():
    data_dir = (
        pathlib.Path(__file__).parent / ".." / ".." / ".." / "src" / "strec" / "data"
    )
    select_conf = data_dir / "select.conf"
    config, results = get_select_config(select_conf)
    assert results
    x = 1


if __name__ == "__main__":
    test_get_config()
    test_get_region_probs()
