"""
Synthetic LANL-style trace generator for SimEDC.
Reproduces the statistical properties of LANL HPC systems 4,5,6,7,8,14
as described in Schroeder & Gibson DSN'06 and the SimEDC paper.
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)

# System specs from the paper (Table 1 in Schroeder & Gibson DSN'06)
# system_id: (num_nodes, num_racks, start_year, trace_years)
SYSTEMS = {
    4:  {"nodes": 128,  "racks": 16, "trace_years": 4.0},
    5:  {"nodes": 128,  "racks": 16, "trace_years": 3.5},
    6:  {"nodes": 256,  "racks": 16, "trace_years": 4.0},
    7:  {"nodes": 256,  "racks": 32, "trace_years": 4.0},
    8:  {"nodes": 512,  "racks": 32, "trace_years": 5.0},
    14: {"nodes": 1024, "racks": 32, "trace_years": 4.5},
}

# Failure model parameters (from SimEDC paper Section 5.1 & Table 1)
# Permanent node failure: Exp(1/125 months) mean = 125 months
PERM_NODE_MTTF_MONTHS    = 125.0
# Transient node failure: Exp(1/4 months) mean = 4 months, duration Exp(1/15 min)
TRANS_NODE_MTTF_MONTHS   = 4.0
TRANS_NODE_REPAIR_MINUTES = 15.0

# Root cause categories (mapping to SimEDC failure types)
TRANSIENT_CAUSES  = ["Network", "Power Outage", "Power Spike", "Maintenance"]
PERMANENT_CAUSES  = ["Disk Drive", "SCSI Controller", "Hardware"]

HOURS_PER_MONTH = 730.5   # average

def generate_system_trace(system_id, config):
    nodes      = config["nodes"]
    racks      = config["racks"]
    years      = config["trace_years"]
    total_hours = years * 8760.0

    records = []

    for node_id in range(nodes):
        rack_id = node_id // (nodes // racks)

        # ── Permanent node failures (exponential inter-arrival) ──
        t = 0.0
        while t < total_hours:
            tti = np.random.exponential(PERM_NODE_MTTF_MONTHS * HOURS_PER_MONTH)
            t  += tti
            if t >= total_hours:
                break
            # repair time depends on cross-rack traffic (simplified: 2-8 hours)
            repair_h = np.random.uniform(2, 8)
            cause    = np.random.choice(PERMANENT_CAUSES)
            records.append({
                "system":      system_id,
                "node":        node_id,
                "rack":        rack_id,
                "start_hours": round(t, 4),
                "end_hours":   round(t + repair_h, 4),
                "failure_type": "permanent_node",
                "root_cause":  cause,
            })
            t += repair_h

        # ── Transient node failures (exponential inter-arrival) ──
        t = 0.0
        while t < total_hours:
            tti = np.random.exponential(TRANS_NODE_MTTF_MONTHS * HOURS_PER_MONTH)
            t  += tti
            if t >= total_hours:
                break
            # duration: exponential with mean 15 minutes
            duration_h = np.random.exponential(TRANS_NODE_REPAIR_MINUTES / 60.0)
            cause      = np.random.choice(TRANSIENT_CAUSES)
            records.append({
                "system":      system_id,
                "node":        node_id,
                "rack":        rack_id,
                "start_hours": round(t, 4),
                "end_hours":   round(t + duration_h, 4),
                "failure_type": "transient_node",
                "root_cause":  cause,
            })
            t += duration_h

    # ── Inject correlated burst failures (mimics Systems 5 & 8 behaviour) ──
    # The paper notes contiguous node failures within 13 hours for System 5
    if system_id in [5, 8]:
        num_bursts = np.random.randint(2, 5)
        for _ in range(num_bursts):
            burst_time  = np.random.uniform(0, total_hours - 24)
            burst_rack  = np.random.randint(0, racks)
            burst_nodes = range(burst_rack * (nodes // racks),
                                (burst_rack + 1) * (nodes // racks))
            # 30-50% of nodes in the rack fail within 13 hours
            affected = np.random.choice(list(burst_nodes),
                                        size=max(2, len(list(burst_nodes)) // 3),
                                        replace=False)
            for n in affected:
                offset = np.random.uniform(0, 13)  # within 13 hours
                records.append({
                    "system":       system_id,
                    "node":         int(n),
                    "rack":         burst_rack,
                    "start_hours":  round(burst_time + offset, 4),
                    "end_hours":    round(burst_time + offset + np.random.uniform(1, 5), 4),
                    "failure_type": "permanent_node",
                    "root_cause":   "Disk Drive",
                })

    df = pd.DataFrame(records)
    df = df.sort_values("start_hours").reset_index(drop=True)
    return df


# ── Generate and save all traces ──────────────────────────────────────────────
os.makedirs("traces", exist_ok=True)

for sid, cfg in SYSTEMS.items():
    print(f"Generating trace for System {sid}  "
          f"({cfg['nodes']} nodes, {cfg['racks']} racks, "
          f"{cfg['trace_years']} years) ...", end=" ")
    df = generate_system_trace(sid, cfg)
    out = f"traces/system{sid}_trace.csv"
    df.to_csv(out, index=False)
    perm  = (df.failure_type == "permanent_node").sum()
    trans = (df.failure_type == "transient_node").sum()
    print(f"done — {len(df)} events  ({perm} permanent, {trans} transient)")
    print(f"  → saved to {out}")

print("\nAll traces generated successfully!")
print("Files in traces/:")
for f in sorted(os.listdir("traces")):
    size = os.path.getsize(f"traces/{f}")
    print(f"  {f}  ({size} bytes)")
