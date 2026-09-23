import textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

PHASES = [
    {
        "title": "PHASE 1",
        "subtitle": "SimEDC restoration\non Python 3.13",
        "color": "#0072B2",
        "items": [
            "SimEDC cloned from the original release",
            "4 Python 3 true-division incompatibilities found in lib/state.py (2 floor-division, 2 range)",
            "All 4 patched with a single sed command",
            "Trace-driven mode requires the -A\u00a0regular flag",
            "Verified on Kali Linux, Python 3.13",
        ],
    },
    {
        "title": "PHASE 2",
        "subtitle": "Synthetic failure\ntrace generation",
        "color": "#009E73",
        "items": [
            "Permanent node failures: exponential, mean 125 months",
            "Transient node failures: every 4 months, 15-minute repair",
            "6 systems (D4-D8, D14), 128 to 1,024 nodes",
            "Burst correlated failures in D5, D8, D14",
            "Cyclic node mapping: trace_id = node_id mod N",
            "Failure rate 8.59-11.13% vs 9.6% target (10.1% pooled)",
        ],
    },
    {
        "title": "PHASE 3",
        "subtitle": "Reproduction and\nvalidation",
        "color": "#CC79A7",
        "items": [
            "RS(9,6) flat r=9, RS(9,6) hierarchical r=3, DRC(9,6,3)",
            "3 configurations x 6 systems = 18 runs",
            "360 iterations per run",
            "Metrics: PDL (95% Wilson CI), NOMDL, BR",
            "5 systems reported; D14 excluded (no differentiation)",
            "Compared with Figure 9 of Zhang et al.",
        ],
    },
]

FOOTER = ("18 simulation runs  |  360 iterations per run  |  "
          "3 erasure-code configurations  |  6 synthetic systems  |  "
          "Kali Linux, Python 3.13")

plt.rcParams.update({"font.family": "serif"})
fig, ax = plt.subplots(figsize=(12, 5.7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.7)
ax.axis("off")

box_w, box_h = 3.4, 4.4
gap = (12 - 3 * box_w) / 4
y0 = 1.0
header_h = 1.05

for i, ph in enumerate(PHASES):
    x0 = gap + i * (box_w + gap)
    ax.add_patch(FancyBboxPatch((x0, y0), box_w, box_h,
                 boxstyle="round,pad=0,rounding_size=0.12",
                 facecolor="white", edgecolor=ph["color"], linewidth=1.8))
    ax.add_patch(FancyBboxPatch((x0, y0 + box_h - header_h), box_w, header_h,
                 boxstyle="round,pad=0,rounding_size=0.12",
                 facecolor=ph["color"], edgecolor=ph["color"], linewidth=1.8))
    ax.text(x0 + box_w / 2, y0 + box_h - 0.28, ph["title"], ha="center",
            va="center", color="white", fontsize=12, fontweight="bold")
    ax.text(x0 + box_w / 2, y0 + box_h - 0.72, ph["subtitle"], ha="center",
            va="center", color="white", fontsize=9.5, style="italic",
            linespacing=1.15)
    ty = y0 + box_h - header_h - 0.25
    for item in ph["items"]:
        lines = textwrap.wrap(item, 36)
        ax.text(x0 + 0.18, ty, "\u2022", ha="left", va="top",
                color=ph["color"], fontsize=10, fontweight="bold")
        ax.text(x0 + 0.38, ty, "\n".join(lines), ha="left", va="top",
                fontsize=8.6, color="#222222", linespacing=1.2)
        ty -= 0.14 + 0.19 * len(lines)
    if i < len(PHASES) - 1:
        xa = x0 + box_w + 0.05
        ax.add_patch(FancyArrowPatch((xa, y0 + box_h / 2),
                     (xa + gap - 0.1, y0 + box_h / 2),
                     arrowstyle="-|>", mutation_scale=18,
                     color="#444444", linewidth=1.6))

ax.add_patch(FancyBboxPatch((gap, 0.25), 12 - 2 * gap, 0.5,
             boxstyle="round,pad=0,rounding_size=0.08",
             facecolor="#f0f0f0", edgecolor="#999999", linewidth=0.8))
ax.text(6, 0.5, FOOTER, ha="center", va="center", fontsize=8.8,
        color="#222222")

for ext in ("png", "pdf", "svg"):
    fig.savefig(f"figure2_methodology.{ext}", dpi=300, bbox_inches="tight")
print("Saved figure2_methodology.png / .pdf / .svg")
