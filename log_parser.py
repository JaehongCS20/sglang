import re
import pandas as pd


fracs = [4, 45, 5, 55, 6, 65, 7, 75, 8, 85, 9]

for frac in fracs:

    log_file_path = f"output_{frac}.log"

    prefill_data = []
    decode_data = []

    prefill_pattern = re.compile(
        r"\[(.*?) TP\d+\] Prefill batch\. #new-seq: (\d+), #new-token: (\d+), #cached-token: (\d+), cache hit rate: ([\d\.]+)%, token usage: ([\d\.]+), #running-req: (\d+), #queue-req: (\d+)"
    )
    decode_pattern = re.compile(
        r"\[(.*?) TP\d+\] Decode batch\. #running-req: (\d+), #token: (\d+), token usage: ([\d\.]+), gen throughput \(token/s\): ([\d\.]+), #queue-req: (\d+)"
    )


    first_prefill_skipped = False

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            prefill_match = prefill_pattern.search(line)
            decode_match = decode_pattern.search(line)

            if prefill_match:
                if not first_prefill_skipped:
                    first_prefill_skipped = True
                    continue

                timestamp, new_seq, new_token, cached_token, cache_hit_rate, token_usage, running_req, queue_req = prefill_match.groups()
                prefill_data.append([timestamp, int(new_seq), int(new_token), int(cached_token), float(cache_hit_rate), float(token_usage), int(running_req), int(queue_req)])

            if decode_match:
                timestamp, running_req, token, token_usage, throughput, queue_req = decode_match.groups()
                decode_data.append([timestamp, int(running_req), int(token), float(token_usage), float(throughput), int(queue_req)])

    prefill_df = pd.DataFrame(prefill_data, columns=["Timestamp", "New Seq", "New Token", "Cached Token", "Cache Hit Rate", "Token Usage", "Running Req", "Queue Req"])
    decode_df = pd.DataFrame(decode_data, columns=["Timestamp", "Running Req", "Token", "Token Usage", "Throughput (token/s)", "Queue Req"])

    prefill_csv_path = f"output_log/prefill_data_{frac}.csv"
    decode_csv_path = f"output_log/decode_data_{frac}.csv"

    prefill_df.to_csv(prefill_csv_path, index=False)
    decode_df.to_csv(decode_csv_path, index=False)