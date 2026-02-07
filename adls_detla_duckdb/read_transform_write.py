import duckdb

con = duckdb.connect()
con.execute("INSTALL delta;")
con.execute("LOAD delta;")

con.execute("""
    COPY (
        SELECT *
        FROM delta_scan(
            'C:/Users/Arulraj Gopal/OneDrive/Desktop/people_delta'
        )
        WHERE first_name <> 'first_name'
          AND id IN (3, 4)
    )
    TO 'C:/Users/Arulraj Gopal/OneDrive/Desktop/people_filtered/people.parquet'
    (FORMAT parquet)
""")

print("successfully written into parquet !!!")