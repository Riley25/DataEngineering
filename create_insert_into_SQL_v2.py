def create_INSERT_INTO_SQL(DATA, table_name):
    # Do NOT fillna("") – we want NaN/None to become SQL NULL
    import pandas as pd
    import numpy as np
    import datetime as dt
    
    columns = ', '.join(DATA.columns)
    values_list = []

    for row in DATA.itertuples(index=False, name=None):
        formatted_row = []

        for value in row:
            # 1) NULL / NaN handling
            if value is None or (isinstance(value, float) and np.isnan(value)):
                formatted_row.append("NULL")

            # 2) Datetime / date handling (pandas Timestamp, datetime, or date)
            elif isinstance(value, (pd.Timestamp, dt.datetime, dt.date)):
                # Format as string Snowflake understands as TIMESTAMP
                s = value.strftime('%Y-%m-%d %H:%M:%S')
                # Let Snowflake implicitly cast it to TIMESTAMP_NTZ
                formatted_row.append(f"'{s}'")
                # If you prefer explicit casting:
                # formatted_row.append(f"TO_TIMESTAMP('{s}')")

            # 3) Strings
            elif isinstance(value, str):
                v = (
                    value.replace("'", "''")
                         .replace("\n", " ")
                         .replace("\r", " ")
                         .replace(";", "")
                )
                formatted_row.append(f"'{v}'")

            # 4) Everything else (numbers, etc.)
            else:
                formatted_row.append(str(value))

        values_list.append(f"({', '.join(formatted_row)})")

    values = ",\n".join(values_list)
    insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES\n{values};"
    return( insert_statement)