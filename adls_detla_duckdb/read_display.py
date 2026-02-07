import duckdb

con = duckdb.connect()
con.execute("INSTALL delta;")
con.execute("LOAD delta;")

query_1 = """
    SELECT *
    FROM delta_scan(
        'C:\\Users\\Arulraj Gopal\\OneDrive\\Desktop\\people_delta'
    )
    WHERE first_name <> 'first_name'
    LIMIT 10
"""

df = con.execute(query_1).df()
print(df)

