"""
SSD/NVMe Failure Trace Generator for SimEDC
Compares against original HDD Weibull model from SimEDC paper

Failure rate sources:
- Backblaze 2023 SSD & NVMe reliability report
  SSD AFR  = 0.98%  → MTTF ~102 years per drive
  NVMe AFR = 0.47%  → MTTF ~213 years per drive
- HDD AFR  = ~4%    → MTTF ~10 years (original SimEDC Weibull model)

Key academic distinction:
- HDD: Weibull distribution — gradual wear-out, predictable degradation
- SSD: Exponential distribution — sudden death, no wear-out phase
- NVMe: Exponential distribution — even lower AFR but equally sudden

References:
- Backblaze (2023). SSD Stats Q4 2023.
- Meza et al. (2015). A Large-Scale Study of Flash Memory Failures
  in the Field. ACM SIGMETRICS.
- Schroeder et al. (2016). Flash Reliability in Production:
  The Expected and the Unexpected. USENIX FAST.
"""
import numpy as np
import pandas as pd
import os

np.random.seed(99)

# ── Simulation constants ──────────────────────────────────────
HOURS_PER_YEAR  = 8760.0
HOURS_PER_MONTH = 730.5

# ── Failure model parameters ─────────────────────────────────
# SSD: Backblaze 2023 measured AFR = 0.98%
SSD_MTTF_HOURS  = (1.0 / 0.0098) * HOURS_PER_YEAR   # ~102 year MTTF

# NVMe: Backblaze 2023 measured AFR = 0.47%
NVME_MTTF_HOURS = (1.0 / 0.0047) * HOURS_PER_YEAR   # ~213 year MTTF

# Transient node failures — same as original SimEDC model
# Keeps comparison fair — only permanent failure model changes
TRANS_NODE_MTTF_HOURS = 4.0 * HOURS_PER_MONTH   # Exp(1/4 months)
TRANS_REPAIR_HOURS    = 0.25                      # Exp(1/15 min) = 0.25 hr

# ── System configurations ─────────────────────────────────────
# Extended to 10 years to match SimEDC mission time
# Necessary to observe statistically meaningful SSD failure events
# given the much lower SSD/NVMe AFR compared to HDD
SYSTEMS = {
    4:  {"nodes": 128,  "racks": 16, "trace_years": 10.0},
    5:  {"nodes": 128,  "racks": 16, "trace_years": 10.0},
    6:  {"nodes": 256,  "racks": 16, "trace_years": 10.0},
    7:  {"nodes": 256,  "racks": 32, "trace_years": 10.0},
    8:  {"nodes": 512,  "racks": 32, "trace_years": 10.0},
    14: {"nodes": 1024, "racks": 32, "trace_years": 10.0},
}


def generate_ssd_trace(system_id, config, drive_type="ssd"):
    """
    Generate synthetic failure traces using SSD or NVMe failure models.

    Unlike HDD Weibull model (gradual wear-out), SSD and NVMe failures
    follow an exponential distribution — modelling sudden death with
    no gradual degradation phase. This reflects the absence of moving
    mechanical parts and the write-endurance cliff in flash storage.
    """
    nodes       = config["nodes"]
    racks       = config["racks"]
    years       = config["trace_years"]
    total_hours = years * HOURS_PER_YEAR

    # Select MTTF based on drive type
    if drive_type == "nvme":
        perm_mttf = NVME_MTTF_HOURS
        root_cause = "NVMe_Sudden_Death"
    else:
        perm_mttf = SSD_MTTF_HOURS
        root_cause = "SSD_Sudden_Death"

    records = []

    for node_id in range(nodes):
        rack_id = node_id // (nodes // racks)

        # ── Permanent failures: Exponential (sudden death) ────────────
        # Unlike HDD Weibull, no increasing hazard rate with age
        # Flash storage fails suddenly — often without prior warning
        t = 0.0
        while t < total_hours:
            tti = np.random.exponential(perm_mttf)
            t  += tti
            if t >= total_hours:
                break
            # SSD replacement is faster than HDD — solid state, no platters
            repair_h = np.random.uniform(0.5, 3.0)
            records.append({
                "system":       system_id,
                "node":         node_id,
                "rack":         rack_id,
                "start_hours":  round(t, 4),
                "end_hours":    round(t + repair_h, 4),
                "failure_type": "permanent_node",
                "root_cause":   root_cause,
                "drive_type":   drive_type
            })
            t += repair_h

        # ── Transient node failures: same as original SimEDC model ─────
        # Keeping transient model constant isolates the effect of
        # changing only the permanent failure distribution
        t = 0.0
        while t < total_hours:
            tti      = np.random.exponential(TRANS_NODE_MTTF_HOURS)
            t       += tti
            if t >= total_hours:
                break
            duration = np.random.exponential(TRANS_REPAIR_HOURS)
            records.append({
                "system":       system_id,
                "node":         node_id,
                "rack":         rack_id,
                "start_hours":  round(t, 4),
                "end_hours":    round(t + duration, 4),
                "failure_type": "transient_node",
                "root_cause":   "Network",
                "drive_type":   drive_type
            })
            t += duration

    df = pd.DataFrame(records)
    df = df.sort_values("start_hours").reset_index(drop=True)
    return df


# ── Generate traces for SSD and NVMe ─────────────────────────
for drive_type in ["ssd", "nvme"]:
    out_dir = f"traces_{drive_type}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'='*55}")
    print(f"  Generating {drive_type.upper()} traces "
          f"(10-year observation period)")
    print(f"{'='*55}")

    total_perm  = 0
    total_trans = 0

    for sid, cfg in SYSTEMS.items():
        df    = generate_ssd_trace(sid, cfg, drive_type)
        out   = f"{out_dir}/system{sid}_trace.csv"
        df.to_csv(out, index=False)

        perm  = (df.failure_type == "permanent_node").sum()
        trans = (df.failure_type == "transient_node").sum()
        total_perm  += perm
        total_trans += trans

        afr_est = (perm / cfg["nodes"]) / cfg["trace_years"] * 100
        print(f"  System {sid:2d} ({cfg['nodes']:4d} nodes, "
              f"{cfg['racks']:2d} racks): "
              f"{perm:4d} permanent  |  "
              f"{trans:5d} transient  |  "
              f"est. AFR = {afr_est:.3f}%")

    print(f"\n  Total permanent failures : {total_perm}")
    print(f"  Total transient failures : {total_trans}")
    print(f"  → Saved to {out_dir}/")

# ── Print academic comparison summary ────────────────────────
print("\n\n" + "="*65)
print("  FAILURE MODEL COMPARISON — ACADEMIC SUMMARY")
print("="*65)
print(f"{'Model':<12} {'Source':<28} {'MTTF':>10} {'AFR':>8} "
      f"{'Distribution'}")
print("-"*65)
print(f"{'HDD':<12} {'LANL traces / Weibull(1.12,10yr)':<28} "
      f"{'10 yrs':>10} {'~4.0%':>8} {'Weibull (wear-out)'}")
print(f"{'SSD':<12} {'Backblaze 2023 production fleet':<28} "
      f"{'102 yrs':>10} {'~0.98%':>8} {'Exponential (sudden)'}")
print(f"{'NVMe':<12} {'Backblaze 2023 production fleet':<28} "
      f"{'213 yrs':>10} {'~0.47%':>8} {'Exponential (sudden)'}")
print("="*65)
print("\nNote: Transient failure model kept identical across all three")
print("drive types to isolate the effect of permanent failure distribution.")
print("\n✅ All traces generated successfully!")
