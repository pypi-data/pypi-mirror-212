#!/usr/bin/env python

# stdlib imports
import pathlib

# third party imports
import numpy as np
import pandas as pd
import pytest

# local imports
from strec.calc import (
    check_moment_row,
    get_input_dataframe,
    get_moment_columns,
    select_regions,
)

ATOL = 0.2
RTOL = 0.9


def compare_tensors(tensor1, tensor2):
    for key, value in tensor1.items():
        cmp_value = tensor2[key]
        if isinstance(value, str):
            assert value == cmp_value
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                np.testing.assert_allclose(
                    subvalue, cmp_value[subkey], rtol=RTOL, atol=ATOL
                )

        else:
            np.testing.assert_allclose(value, cmp_value, rtol=RTOL, atol=ATOL)


def test_get_moment_columns():
    row = pd.Series(
        {
            "Mrr": 147400000000000,
            "Mtt": -534500000000000,
            "Mpp": 387100000000000,
            "Mrp": 282800000000000,
            "Mrt": -65680000000000,
            "Mtp": -249700000000000,
        }
    )
    tensor_params = get_moment_columns(row)
    cmp_params = {
        "mrr": 147400000000000.0,
        "mtt": -534500000000000.0,
        "mpp": 387100000000000.0,
        "mrt": -65680000000000.0,
        "mrp": 282800000000000.0,
        "mtp": -249700000000000.0,
        "source": "unknown",
        "type": "unknown",
        "NP1": {
            "strike": 296.30077024634284,
            "dip": 68.11685306165077,
            "rake": 157.15208404514294,
        },
        "NP2": {
            "strike": 35.225709774290436,
            "dip": 68.88083955258415,
            "rake": 23.55014283538641,
        },
        "T": {
            "azimuth": 255.93919800048124,
            "value": 626337818224371.0,
            "plunge": 31.22002840266667,
        },
        "N": {
            "azimuth": 74.80537317180232,
            "value": -28481000172499.133,
            "plunge": 58.77499824283217,
        },
        "P": {
            "azimuth": 165.63454565853377,
            "value": -597856818051871.8,
            "plunge": 0.5026289265483992,
        },
    }
    compare_tensors(tensor_params, cmp_params)
    row = pd.Series(
        {
            "Strike": 1,
            "Dip": 1,
            "Rake": 1,
        }
    )
    tensor_params = get_moment_columns(row)
    cmp_params = {
        "mrr": 766786542744639.8,
        "mtt": -766903310262146.4,
        "mpp": 116767517506.37914,
        "mrt": -1.2587334961693614e18,
        "mrp": 10036448003488.078,
        "mtp": -2.196792959061808e16,
        "source": "unknown",
        "type": "unknown",
        "NP1": {
            "strike": 0.9999999997718305,
            "dip": 0.9999999997715706,
            "rake": 0.9999999997715463,
        },
        "NP2": {
            "strike": 270.00015227392294,
            "dip": 89.98254847933853,
            "rake": 90.99984772584894,
        },
        "T": {
            "azimuth": 181.00015232031038,
            "value": 1.2589254117941714e18,
            "plunge": 45.00872576013233,
        },
        "N": {
            "azimuth": 89.99984770289579,
            "value": -0.17311440291958194,
            "plunge": 0.999847679693138,
        },
        "P": {
            "azimuth": 359.00076099885496,
            "value": -1.2589254117941714e18,
            "plunge": 44.97382803145975,
        },
    }
    compare_tensors(tensor_params, cmp_params)


def test_check_moment_row():
    row = pd.Series(
        {
            "Mrr": 1,
            "Mtt": 1,
            "Mpp": 1,
            "Mrp": 1,
            "Mrt": 1,
            "Mtp": 1,
        }
    )
    assert check_moment_row(row)
    row = pd.Series(
        {
            "Strike": 1,
            "Dip": 1,
            "Rake": 1,
        }
    )
    assert check_moment_row(row)
    row = pd.Series(
        {
            "Dip": 1,
            "Rake": 1,
        }
    )
    assert not check_moment_row(row)


def test_get_input_dataframe():
    simple_catalog_file = pathlib.Path(__file__).parent / "data" / "simple_catalog.xlsx"
    eqinfo = None
    event_id = None
    hypo_columns = [None, None, None, None]
    id_column = None
    simple_dataframe, _, _, _, _, _ = get_input_dataframe(
        simple_catalog_file, eqinfo, event_id, hypo_columns, id_column
    )
    cmp_simple = pd.DataFrame(
        {
            "Latitude": [-5.074, -1.008],
            "Longitude": [103.083, 98.642],
            "Depth": [50.5, 17.6],
            "Magnitude": [6.5, 6.5],
        }
    )
    assert simple_dataframe.equals(cmp_simple)

    comcat_catalog_file = (
        pathlib.Path(__file__).parent / "data" / "comcatid_catalog.xlsx"
    )
    eqinfo = None
    event_id = None
    hypo_columns = [None, None, None]
    id_column = None
    comcat_dataframe, idcol, _, _, _, _ = get_input_dataframe(
        comcat_catalog_file, eqinfo, event_id, hypo_columns, id_column
    )
    assert idcol == "EventID"

    id_catalog_file = pathlib.Path(__file__).parent / "data" / "id_catalog.xlsx"
    eqinfo = None
    event_id = None
    hypo_columns = [None, None, None, None]
    id_column = "id"
    comcat_dataframe, idcol, _, _, _, _ = get_input_dataframe(
        id_catalog_file, eqinfo, event_id, hypo_columns, id_column
    )
    assert idcol == "id"

    hypo_catalog_file = pathlib.Path(__file__).parent / "data" / "hypocols_catalog.xlsx"
    eqinfo = None
    event_id = None
    hypo_columns = ["EventLatitude", "EventLongitude", "EventDepth", "magnitude"]
    id_column = None
    hypo_dataframe, idcol, latcol, loncol, depcol, magcol = get_input_dataframe(
        hypo_catalog_file, eqinfo, event_id, hypo_columns, id_column
    )
    assert [latcol, loncol, depcol, magcol] == hypo_columns

    moment_catalog_file = pathlib.Path(__file__).parent / "data" / "moment_catalog.xlsx"
    eqinfo = None
    event_id = None
    hypo_columns = [None, None, None, None]
    id_column = None
    moment_dataframe, _, _, _, _, _ = get_input_dataframe(
        moment_catalog_file, eqinfo, event_id, hypo_columns, id_column
    )
    assert "mrt" in moment_dataframe.columns

    focal_catalog_file = pathlib.Path(__file__).parent / "data" / "focal_catalog.xlsx"
    eqinfo = None
    event_id = None
    hypo_columns = [None, None, None, None]
    id_column = None
    focal_dataframe, _, _, _, _, _ = get_input_dataframe(
        focal_catalog_file, eqinfo, event_id, hypo_columns, id_column
    )
    assert "strike" in focal_dataframe.columns


def test_select_regions():
    simple_catalog_file = pathlib.Path(__file__).parent / "data" / "simple_catalog.xlsx"
    eqinfo = None
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = [None, None, None, None]
    id_column = None
    simple_dataframe = select_regions(
        simple_catalog_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    assert simple_dataframe["TectonicRegion"].unique().tolist() == ["Subduction"]
    assert (simple_dataframe["KaganAngle"] < 15).all()

    comcat_catalog_file = (
        pathlib.Path(__file__).parent / "data" / "comcatid_catalog.xlsx"
    )
    eqinfo = None
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = [None, None, None, None]
    id_column = None
    comcat_dataframe = select_regions(
        comcat_catalog_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    assert comcat_dataframe["FocalMechanism"].to_list() == ["RS", "SS"]

    id_catalog_file = pathlib.Path(__file__).parent / "data" / "id_catalog.xlsx"
    eqinfo = None
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = [None, None, None, None]
    id_column = "id"
    id_dataframe = select_regions(
        id_catalog_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    assert id_dataframe["FocalMechanism"].to_list() == ["RS", "SS"]

    hypo_catalog_file = pathlib.Path(__file__).parent / "data" / "hypocols_catalog.xlsx"
    eqinfo = None
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = ["EventLatitude", "EventLongitude", "EventDepth", "magnitude"]
    id_column = None
    hypo_dataframe = select_regions(
        hypo_catalog_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    assert hypo_dataframe["FocalMechanism"].to_list() == ["RS", "SS"]

    moment_catalog_file = pathlib.Path(__file__).parent / "data" / "moment_catalog.xlsx"
    eqinfo = None
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = [None, None, None, None]
    id_column = None
    moment_dataframe = select_regions(
        moment_catalog_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    assert moment_dataframe["FocalMechanism"].to_list() == ["RS", "SS"]

    focal_catalog_file = pathlib.Path(__file__).parent / "data" / "focal_catalog.xlsx"
    eqinfo = None
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = [None, None, None, None]
    id_column = None
    focal_dataframe = select_regions(
        focal_catalog_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    assert focal_dataframe["FocalMechanism"].to_list() == ["RS", "SS"]

    eqinfo = [37.7132, 141.5793, 41, 6.5]
    event_id = None
    moment_info = [None, None, None, None]
    hypo_columns = [None, None, None, None]
    id_column = None
    eq_dataframe = select_regions(
        None,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        False,
    )
    eq_dataframe.iloc[0]["FocalMechanism"] == "RS"


if __name__ == "__main__":
    test_get_moment_columns()
    test_check_moment_row()
    test_get_input_dataframe()
    test_select_regions()
