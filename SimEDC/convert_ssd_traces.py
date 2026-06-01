"""
Converts SSD and NVMe CSV traces into SimEDC .txt format
Same cyclic mapping approach as original HDD trace conversion
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

SIMEDC_TOTAL_NODES = 1024

def convert_traces(trace_dir, output_base):
    """Convert CSV traces to SimEDC per-node .txt files"""

    # Create output directories
    for folder in ["failure_events", "transient_events", "transient_repair"]:
        os.makedirs(f"{output_base}/{folder}", exist_ok=True)

    print(f"\nConverting traces from {trace_dir}/ → {output_base}/")
    print("="*55)

    for system_id, trace_id in SYSTEM_TO_TRACEID.items():
        csv_path = f"{trace_dir}/system{system_id}_trace.csv"
        df       = pd.read_csv(csv_path)

        actual_nodes = sorted(df["node"].unique())
        num_actual   = len(actual_nodes)

        perm_count  = 0
        trans_count = 0

        for simedc_node in range(SIMEDC_TOTAL_NODES):
            # Cyclic mapping — same method as HDD traces
            source_node = actual_nodes[simedc_node % num_actual]
            node_df     = df[df["node"] == source_node].sort_values("start_hours")

            # ── Permanent failures ─────────────────────────────
            perm       = node_df[node_df["failure_type"] == "permanent_node"]
            perm_times = sorted(perm["start_hours"].tolist())

            with open(f"{output_base}/failure_events/s{trace_id}n{simedc_node}.txt", "w") as f:
                for t in perm_times:
                    f.write(f"{t}\n")
            if perm_times:
                perm_count += 1

            # ── Transient failures ─────────────────────────────
            trans          = node_df[node_df["failure_type"] == "transient_node"].sort_values("start_hours")
            trans_start    = trans["start_hours"].tolist()
            trans_duration = (trans["end_hours"] - trans["start_hours"]).tolist()

            with open(f"{output_base}/transient_events/s{trace_id}n{simedc_node}.txt", "w") as f:
                for t in trans_start:
                    f.write(f"{t}\n")

            with open(f"{output_base}/transient_repair/s{trace_id}n{simedc_node}.txt", "w") as f:
                for d in trans_duration:
                    f.write(f"{d}\n")

            if trans_start:
                trans_count += 1

        print(f"  System {system_id:2d} → trace_id {trace_id}: "
              f"{num_actual} actual nodes → {SIMEDC_TOTAL_NODES} SimEDC nodes "
              f"| {perm_count} nodes w/ permanent failures")

    # Verify
    fe = len(os.listdir(f"{output_base}/failure_events"))
    te = len(os.listdir(f"{output_base}/transient_events"))
    tr = len(os.listdir(f"{output_base}/transient_repair"))
    print(f"\n  ✅ failure_events : {fe} files")
    print(f"  ✅ transient_events: {te} files")
    print(f"  ✅ transient_repair: {tr} files")


# ── Convert both SSD and NVMe ─────────────────────────────────
convert_traces("traces_ssd",  "tracelib_ssd")
convert_traces("traces_nvme", "tracelib_nvme")

print("\n🎉 All SSD and NVMe trace files converted successfully!")
