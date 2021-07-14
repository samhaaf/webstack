
import psycopg2


def execute(connection, statement, values=None, batch_size=100, catch=False, num_tries=3):

    for attempt in range(num_tries):
        cursor = connection.cursor()
        try:
            if values is not None:
                cursor.execute(statement, values)
            else:
                cursor.execute(statement)
            break
        except Exception as e:
            if attempt < num_tries - 1:
                continue
            if catch:
                return e, None
            else:
                raise e

    columns = []
    results = []
    if cursor.description is not None:
        columns = [desc[0] for desc in cursor.description]
        while True:
            batch = cursor.fetchmany(batch_size)
            if len(batch) == 0:
                break
            results += [{c: v for c, v in zip(columns, row)} for row in batch]

    cursor.close()

    if catch:
        return None, results
    else:
        return results


def execute_insert_from_dict_list(connection, table_name, dict_list, catch=False, returning=False):
    colnames = list(set(sum([list(row.keys()) for row in dict_list], [])))
    rows = [[row.get(col) for col in colnames] for row in dict_list]
    statement = f"""
        INSERT INTO "{table_name}" ({",".join(colnames)})
        VALUES {",".join(["(" + ",".join(["%s"] * len(row)) + ")" for row in rows])}
    """
    if returning:
        statement += '\nRETURNING *'
    return execute(connection, statement, sum(rows, []), catch=catch)
