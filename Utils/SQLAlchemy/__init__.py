import pandas as pd
from sqlalchemy import types

def format_dataframe(df, dtype_map, format_index = False):
    
    if format_index:
        index_names = df.index.names
        df = df.reset_index(drop=False)
    
    df_columns = df.columns
    for col, dtype in dtype_map.items():
        if col not in df_columns:
            continue

        if isinstance(dtype, types.DateTime):
            # use pandas to_datetime to format datetime columns
            df[col] = pd.to_datetime(df[col])
        elif isinstance(dtype, (types.Integer, types.Float, types.Numeric)):
            # use pandas to_numeric to format numeric columns
            dc_type = 'signed'
            if isinstance(dtype, (types.Float, types.Numeric)):
                dc_type = 'float'
            df[col] = pd.to_numeric(df[col], downcast=dc_type, errors='coerce')
        else:
            # convert other columns to string dtype
            df[col] = df[col].astype(str)
    
    if format_index:
        df = df.set_index(index_names)
    return df
