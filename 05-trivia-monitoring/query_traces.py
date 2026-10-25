import os
from datetime import datetime, timedelta, timezone

import dotenv
from logfire.query_client import LogfireQueryClient

dotenv.load_dotenv("/workspaces/.codespaces/shared/.env")

client = LogfireQueryClient(
    read_token=os.getenv("LOGFIRE_READ_TOKEN")
)

result = client.query_json_rows(
    sql="""
        SELECT trace_id, start_timestamp, span_name
        FROM records
        WHERE span_name = 'trivia_session'
        ORDER BY start_timestamp DESC
        LIMIT 10
    """,
    min_timestamp=datetime.now(timezone.utc) - timedelta(days=7),
)

for row in result["rows"]:
    print(row)