"""
Fixes the node count mismatch.
SimEDC expects 1024 nodes (32 racks × 32 nodes).
Our traces only have 128-1024 nodes per system.
We cycle/repeat node trace data to cover all 1024 nodes.
"""
import pandas as pd
import os

SYSTEM_TO_TRACEID = {
    4:  4,
    5:  5,
    6:  6,
    7:  7,
    8:  8,
    14: 13,
}

SIMEDC_TOTAL_NODES = 1024  # SimEDC default: 32 racks × 32 nodes

for folder in ["failure_events", "transient_events", "transient_repair"]:
    os.makedirs(f"lib/tracelib/{folder}", exist_ok=True)

for system_id, trace_id in SYSTEM_TO_TRACEID.items():
    csv_path = f"traces/system{system_id}_trace.csv"
    print(f"\nSystem {system_id} → trace_id {trace_id}")

    df = pd.read_csv(csv_path)
    actual_nodes = sorted(df["node"].unique())
    num_actual   = len(actual_nodes)
    print(f"  Actual nodes in trace: {num_actual}  |  SimEDC needs: {SIMEDC_TOTAL_NODES}")

    for simedc_node in range(SIMEDC_TOTAL_NODES):
        # Cycle: map SimEDC node 0-1023 onto our actual nodes
        source_node = actual_nodes[simedc_node % num_actual]
        node_df = df[df["node"] == source_node].sort_values("start_hours")

        # ── Permanent failures ─────────────────────────────────
        perm = node_df[node_df["failure_type"] == "permanent_node"]
        perm_times = sorted(perm["start_hours"].tolist())

        with open(f"lib/tracelib/failure_events/s{trace_id}n{simedc_node}.txt", "w") as f:
            for t in perm_times:
                f.write(f"{t}\n")

        # ── Transient failures ─────────────────────────────────
        trans = node_df[node_df["failure_type"] == "transient_node"].sort_values("start_hours")
        trans_start    = trans["start_hours"].tolist()
        trans_duration = (trans["end_hours"] - trans["start_hours"]).tolist()

        with open(f"lib/tracelib/transient_events/s{trace_id}n{simedc_node}.txt", "w") as f:
            for t in trans_start:
                f.write(f"{t}\n")

        with open(f"lib/tracelib/transient_repair/s{trace_id}n{simedc_node}.txt", "w") as f:
            for d in trans_duration:
                f.write(f"{d}\n")

    # Verify
    fe_count = len([x for x in os.listdir("lib/tracelib/failure_events")
                    if x.startswith(f"s{trace_id}n")])
    print(f"  ✅ Written {fe_count} failure_event files for trace_id {trace_id}")

print("\n✅ All trace files fixed and ready!")
print(f"   Total failure_events files : {len(os.listdir('lib/tracelib/failure_events'))}")
print(f"   Total transient_events files: {len(os.listdir('lib/tracelib/transient_events'))}")
print(f"   Total transient_repair files: {len(os.listdir('lib/tracelib/transient_repair'))}")
