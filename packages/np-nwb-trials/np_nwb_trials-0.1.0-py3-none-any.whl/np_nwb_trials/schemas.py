import pandera as pa
from pandera.typing import Index, DataFrame, Series


class TrialsTable(pa.DataFrameModel):
    start_time: Series[float] = pa.Field(coerce=True)
    stop_time: Series[float] = pa.Field(coerce=True)
    is_receptive_field_mapping: Series[bool] = pa.Field(coerce=True)
    # trialStartFrame: Series[int] = pa.Field(coerce=True)
    # trialEndFrame: Series[int] = pa.Field(coerce=True)