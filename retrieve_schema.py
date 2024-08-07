from database import PostgreSQLConnector

def schema():
    query = """SELECT t.table_name AS "Table", STRING_AGG(DISTINCT c.column_name || ' ' || c.data_type, ', ') AS "Columns", STRING_AGG(DISTINCT CONCAT('References ', ccu.table_name, '(', kcu.column_name, ') on ', tc.table_name, '(', kcu.column_name, ')'), ', ') AS "Relations" FROM information_schema.tables t JOIN information_schema.columns c ON t.table_name = c.table_name LEFT JOIN information_schema.table_constraints tc ON t.table_name = tc.table_name AND tc.constraint_type = 'FOREIGN KEY' LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name LEFT JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name WHERE t.table_schema = 'public' GROUP BY t.table_name;"""
    db = PostgreSQLConnector()
    xx = db.execute_query(query)

    # Open a file for writing
    with open("create_tables.sql", "w") as file:
        for item in xx:
            table_name = item[0]
            column_info = item[1]
            relations_info = item[2]
            create_table_statement = f"CREATE TABLE {table_name} (\n"
            for column in column_info.split(', '):
                create_table_statement += f"    {column},\n"
            create_table_statement = create_table_statement.rstrip(",\n") + "\n"
            create_table_statement += f"    PRIMARY KEY ({table_name}_id),\n"
            create_table_statement += f"    UNIQUE ({table_name}_id)\n"
            create_table_statement += ");\n\n"
            file.write(create_table_statement)