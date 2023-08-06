import os
import dotenv
import pathlib
import pytest
import uuid
import datetime
from pynwb import NWBFile
from np_nwb_trials import processing, nwb


dotenv.load_dotenv()

STORAGE_DIRECTORY = pathlib.Path(os.environ["STORAGE_DIR"])

@pytest.mark.skipif(
    not STORAGE_DIRECTORY.exists(),
    reason="Storage directory doesnt exist."
)
def test_append_trials_to_nwb():
    trials_table = processing.storage_directory_to_trials_table(
        str(STORAGE_DIRECTORY),
    )
    nwb_file = NWBFile(
        identifier=uuid.uuid4().hex,
        session_description='Data and metadata for a Neuropixels session',
        session_start_time=datetime.datetime.now(),
    )
    trials_table = nwb.append_trials_to_nwb(
        trials_table,
        nwb_file,
    )
