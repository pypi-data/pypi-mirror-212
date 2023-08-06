#!/usr/bin/env python
# stdlib imports
import pathlib

# third party imports
import numpy as np

# local imports
from strec.slab import GridSlab, SlabCollection
from strec.utils import get_config


def test_grid_slab():
    LAT, LON = -16.342671, 167.541593
    datadir = pathlib.Path(__file__).parent / "data"
    depthgrid = datadir / "van_slab2_dep_02.23.18.grd"
    dipgrid = datadir / "van_slab2_dip_02.23.18.grd"
    strgrid = datadir / "van_slab2_str_02.23.18.grd"
    uncgrid = datadir / "van_slab2_unc_02.23.18.grd"
    grid = GridSlab(depthgrid, dipgrid, strgrid, uncgrid)
    is_inside = grid.contains(LAT, LON)
    assert is_inside

    slabinfo = grid.getSlabInfo(LAT, LON)
    if not len(slabinfo):
        raise AssertionError("Slab results are empty!")
    cmp_dict = {
        "region": "van",
        "strike": 340.6477,
        "dip": 31.101204,
        "depth": 33.961307525634766,
        "maximum_interface_depth": 49,
        "depth_uncertainty": 18.315662,
    }
    for key, value in cmp_dict.items():
        value2 = slabinfo[key]
        print(f"Comparing {key} cmp {value} and actual {value2}")
        if isinstance(value, float):
            np.testing.assert_almost_equal(value, value2, decimal=4)
        else:
            assert value == value2
    print("First test successful")

    collection = SlabCollection(datadir)
    depth = 0.0
    slabinfo = collection.getSlabInfo(LAT, LON, depth)
    if not len(slabinfo):
        raise AssertionError("Slab results are empty!")
    print("Testing against slab grid...")
    for key, value in slabinfo.items():
        assert key in cmp_dict
        if isinstance(value, str):
            assert value == cmp_dict[key]
        else:
            np.testing.assert_almost_equal(value, cmp_dict[key], decimal=1)
    print("Second test successful.")


if __name__ == "__main__":
    test_grid_slab()
