import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from excel_creator import ExcelCreator


def test_create_msa_df():
    creator = ExcelCreator(modules=2, tests=3)
    creator.create_msa_df()

    assert len(creator.msa_data) == 6
    assert "Operator" in creator.msa_data.columns
    assert "Part" in creator.msa_data.columns


def test_create_tolerance_df():
    creator = ExcelCreator()
    components = ["R1", "C1", "U1"]

    creator.create_tolerance_df(components)

    assert len(creator.tolerance_data) == 3
    assert "Designator" in creator.tolerance_data.columns
    assert "Tolerance X" in creator.tolerance_data.columns


def test_data_filter_basic():
    creator = ExcelCreator(modules=1, tests=2)
    creator.create_msa_df()

    # fake CSV data
    df = pd.DataFrame({
        "ModuleID": [1, 1],
        "Location Name": ["R1", "R1"],
        "OffsetX": [1000, 2000],
        "OffsetY": [3000, 4000]
    })

    creator.data_filter(df, ["R1"], "TOP")

    # check new columns
    assert "TOP_R1_X" in creator.msa_data.columns
    assert "TOP_R1_Y" in creator.msa_data.columns

    # check conversion (µm → mm)
    assert creator.msa_data["TOP_R1_X"].iloc[0] == 1.0