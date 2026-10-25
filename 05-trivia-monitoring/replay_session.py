import os
from datetime import datetime, timedelta, timezone

import dotenv
from logfire.query_client import LogfireQueryClient

import trace_replay

dotenv.load_dotenv("/workspaces/.codespaces/shared/.env")

client = LogfireQueryClient(
    read_token=os.getenv("LOGFIRE_READ_TOKEN")
)

trace_id = "01a1728efb5d308c39c8b59a19d40c24"

trace = trace_replay.fetch_trace(trace_id, client)
run = trace_replay.trace_to_run_result(trace)

print("Result type:", type(run).__name__)
print("Input tokens:", trace.input_tokens)
print("Output tokens:", trace.output_tokens)

cost = (
    trace.input_tokens * 0.15
    + trace.output_tokens * 0.60
) / 1_000_000

print(f"Estimated cost: ${cost:.6f}")