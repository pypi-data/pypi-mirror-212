import pandas as pd
import pandera as pa
import logging
from pynwb import NWBFile

from .utils import dict_to_indexed_array
from .. import schemas


logger = logging.getLogger(__name__)


DESCRIPTIONS = {
    "start_time": "Trial start time in seconds since start of experiment.",
    "stop_time": "Trial stop time in seconds since start of experiment.",
    "is_receptive_field_mapping": "",
}


def get_column_description(name: str) -> str:
    try:
        return DESCRIPTIONS[name]
    except KeyError:
        return f"Unsupported description: {name}."


@pa.check_types
def append_trials_to_nwb(
    trials: pa.typing.DataFrame[schemas.TrialsTable],
    nwbfile: NWBFile,
) -> NWBFile:
    """
    Returns
    -------
    nwbfile with trials_df appended

    Notes
    -----
    - intended for import
    """
    order = list(trials.index)
    for _, row in trials[["start_time", "stop_time"]].iterrows():
        row_dict = row.to_dict()
        nwbfile.add_trial(**row_dict)

    for c in trials.columns:
        if c in ["start_time", "stop_time"]:
            continue
        index, data = dict_to_indexed_array(trials[c].to_dict(), order)
        if data.dtype == "<U1":  # data type is composed of unicode
            # characters
            data = trials[c].tolist()
        if not len(data) == len(order):
            if len(data) == 0:
                data = [""]
            nwbfile.add_trial_column(
                name=c, description="NOT IMPLEMENTED: %s" % c, data=data, index=index
            )
        else:
            nwbfile.add_trial_column(
                name=c, description="NOT IMPLEMENTED: %s" % c, data=data
            )

    return nwbfile