def create_INSERT_INTO_SQL(DATA , table_name):
        
    DATA = DATA.fillna("")
    columns = ', '.join(DATA.columns)
    values_list = []
    
    for row in DATA.itertuples(index=False, name=None):
        formatted_row = []
        
        for value in row:
            if isinstance(value, str):
                # Replace common special characters
                value = value.replace("'", "''").replace("\n", " ").replace("\r", " ").replace(";","")
                formatted_row.append(f"'{value}'")
            else:
                formatted_row.append(repr(value))
                
        values_list.append(f"({', '.join(formatted_row)}) ")

        # human-readable SQL 
        # values_list.append(f"\n({', '.join(formatted_row)}) ")
    values = ", ".join(values_list)
    
    insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES {values}"
    return(insert_statement)