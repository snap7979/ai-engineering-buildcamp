import os
import urllib.request
import duckdb

DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
PARQUET_FILE = "yellow_tripdata_2024-01.parquet"

con = duckdb.connect("taxi.db")


def setup_database():
    if not os.path.exists(PARQUET_FILE):
        print("Downloading taxi dataset...")
        urllib.request.urlretrieve(DATA_URL, PARQUET_FILE)

    con.execute(f"""
        CREATE TABLE IF NOT EXISTS trips AS
        SELECT * FROM '{PARQUET_FILE}'
    """)

    count = con.execute(
        "SELECT COUNT(*) FROM trips"
    ).fetchone()[0]

    print(f"Loaded {count} rows")
    return count


if __name__ == "__main__":
    setup_database()


class SQLTools:
    def get_schema(self) -> str:
        """Return the columns and types of the trips table."""
        rows = con.execute("DESCRIBE trips").fetchall()
        return "\n".join(f"{name}: {dtype}" for name, dtype, *_ in rows)

    def run_sql(self, query: str) -> str:
        """Execute a read-only SQL query and return up to 50 rows."""
        if not query.strip().lower().startswith(("select", "with")):
            return "Error: Only SELECT queries are allowed."

        try:
            result = con.execute(query)
            columns = [col[0] for col in result.description]
            rows = result.fetchmany(50)
            return "\t".join(columns) + "\n" + "\n".join(
                "\t".join(str(value) for value in row) for row in rows
            )
        except Exception as exc:
            return f"SQL error: {exc}"
