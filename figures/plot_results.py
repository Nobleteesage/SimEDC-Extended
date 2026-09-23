import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N_ITER = 360
CONFIGS = ["RS(9,6) r=9", "RS(9,6) r=3", "DRC(9,6,3)"]
COLORS = ["#D55E00", "#E69F00", "#0072B2"]
HATCH = ["", "//", ".."]

df = pd.read_csv("results.csv")
systems = list(dict.fromkeys(df["system"]))

def wilson(p, n, z=1.96):
    k = p * n
    centre = (k + z**2 / 2) / (n + z**2)
    half = z * np.sqrt(k * (n - k) / n + z**2 / 4) / (n + z**2)
    return centre - half, centre + half

plt.rcParams.update({"font.family": "serif", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), constrained_layout=True)
x = np.arange(len(systems))
w = 0.26

for ax, metric, label, log in [(axes[0], "pdl", "PDL", True),
                               (axes[1], "nomdl", "NOMDL", True),
                               (axes[2], "br", "Blocked Ratio", False)]:
    for i, cfg in enumerate(CONFIGS):
        sub = df[df["config"] == cfg].set_index("system").loc[systems]
        y = sub[metric].values
        yerr = None
        if metric == "pdl":
            lo, hi = zip(*[wilson(p, N_ITER) for p in y])
            yerr = [y - np.array(lo), np.array(hi) - y]
        ax.bar(x + (i - 1) * w, y, w, color=COLORS[i], hatch=HATCH[i],
               edgecolor="black", linewidth=0.5, label=cfg,
               yerr=yerr, capsize=2, error_kw={"linewidth": 0.8})
    ax.set_xticks(x, systems)
    ax.set_xlabel("Synthetic system")
    ax.set_ylabel(label)
    if log:
        ax.set_yscale("log")
    ax.grid(axis="y", linestyle=":", linewidth=0.5)

axes[0].set_title("(a) PDL (95% Wilson CI)")
axes[1].set_title("(b) NOMDL")
axes[2].set_title("(c) BR")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 1.12))
for ext in ("png", "pdf", "svg"):
    fig.savefig(f"figure1_reliability.{ext}", dpi=300, bbox_inches="tight")

fig2, ax = plt.subplots(figsize=(6, 3.6), constrained_layout=True)
for i, cfg in enumerate(CONFIGS):
    sub = df[df["config"] == cfg].set_index("system").loc[systems]
    ax.bar(x + (i - 1) * w, sub["nomdl"] / sub["pdl"], w, color=COLORS[i],
           hatch=HATCH[i], edgecolor="black", linewidth=0.5, label=cfg)
ax.set_xticks(x, systems)
ax.set_xlabel("Synthetic system")
ax.set_ylabel("NOMDL / PDL")
ax.set_title("Data lost per loss event")
ax.grid(axis="y", linestyle=":", linewidth=0.5)
ax.legend(frameon=False, fontsize=8)
for ext in ("png", "pdf", "svg"):
    fig2.savefig(f"figure3_loss_given_loss.{ext}", dpi=300, bbox_inches="tight")
print("Figures saved.")
