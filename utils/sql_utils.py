import sqlite3


def parse_query(query: str) -> str:
    # Convert the query to uppercase and find the first occurrence of SELECT (case insensitive)
    select_position = query.upper().find("SELECT")

    # If SELECT is not found, return the original query
    if select_position == -1:
        return query

    # Remove everything before the first occurrence of SELECT
    query = query[select_position:]

    # Look for the first semicolon and remove everything after that
    semicolon_position = query.find(";")
    if semicolon_position != -1:
        query = query[:semicolon_position]

    return query


def return_sqlite_results(db: str = "./data/my_database.db", query: str = "") -> str:
    """Return the results of a sqlite query"""
    conn = sqlite3.connect(db)
    query = parse_query(query)
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    return results


# Test example
if __name__ == "__main__":
    results = return_sqlite_results(
        query="SELECT avgtemperaturec FROM Temperature WHERE city = 'Madrid' AND month = 6 AND year = 2020;"
    )
    print(results)
