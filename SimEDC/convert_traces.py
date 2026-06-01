"""
Converts generated CSV traces into the .txt format SimEDC expects.
SimEDC reads per-node files from:
  lib/tracelib/failure_events/s{trace_id}n{node_id}.txt   (permanent)
  lib/tracelib/transient_events/s{trace_id}n{node_id}.txt (transient starts)
  lib/tracelib/transient_repair/s{trace_id}n{node_id}.txt (transient durations)
"""
import pandas as pd
import os

# Map our system IDs to SimEDC trace_ids (valid range: 4-11, 13-18)
SYSTEM_TO_TRACEID = {
    4:  4,
    5:  5,
    6:  6,
    7:  7,
    8:  8,
    14: 13,
}

# Create required directories
for folder in ["failure_events", "transient_events", "transient_repair"]:
    os.makedirs(f"lib/tracelib/{folder}", exist_ok=True)
print("✅ Directories ready.\n")

total_perm_files  = 0
total_trans_files = 0

for system_id, trace_id in SYSTEM_TO_TRACEID.items():
    csv_path = f"traces/system{system_id}_trace.csv"
    print(f"Processing System {system_id} → trace_id {trace_id} ...", end=" ")

    df = pd.read_csv(csv_path)
    nodes = sorted(df["node"].unique())

    perm_count  = 0
    trans_count = 0

    for node_id in nodes:
        node_df = df[df["node"] == node_id].sort_values("start_hours")

        # ── Permanent failures ─────────────────────────────────────
        perm = node_df[node_df["failure_type"] == "permanent_node"]
        perm_times = sorted(perm["start_hours"].tolist())

        fname_perm = f"lib/tracelib/failure_events/s{trace_id}n{node_id}.txt"
        with open(fname_perm, "w") as f:
            for t in perm_times:
                f.write(f"{t}\n")
        if perm_times:
            perm_count += 1

        # ── Transient failures ─────────────────────────────────────
        trans = node_df[node_df["failure_type"] == "transient_node"].copy()
        trans = trans.sort_values("start_hours")
        trans_start    = trans["start_hours"].tolist()
        trans_duration = (trans["end_hours"] - trans["start_hours"]).tolist()

        fname_trans = f"lib/tracelib/transient_events/s{trace_id}n{node_id}.txt"
        with open(fname_trans, "w") as f:
            for t in trans_start:
                f.write(f"{t}\n")

        fname_repair = f"lib/tracelib/transient_repair/s{trace_id}n{node_id}.txt"
        with open(fname_repair, "w") as f:
            for d in trans_duration:
                f.write(f"{d}\n")

        if trans_start:
            trans_count += 1

    total_perm_files  += perm_count
    total_trans_files += trans_count
    print(f"done — {len(nodes)} nodes | {perm_count} w/ perm failures | {trans_count} w/ transient failures")

print("\n✅ All trace files converted successfully!")
print(f"   failure_events/  : {len(os.listdir('lib/tracelib/failure_events'))} files")
print(f"   transient_events/: {len(os.listdir('lib/tracelib/transient_events'))} files")
print(f"   transient_repair/: {len(os.listdir('lib/tracelib/transient_repair'))} files")
