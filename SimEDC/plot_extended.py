import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Systems ───────────────────────────────────────────────────
systems    = [4, 5, 6, 7, 8, 14]
trace_ids  = [4, 5, 6, 7, 8, 13]
sys_labels = [
    "System 4\n(128 nodes\n16 racks)",
    "System 5\n(128 nodes\n16 racks)",
    "System 6\n(256 nodes\n16 racks)",
    "System 7\n(256 nodes\n32 racks)",
    "System 8\n(512 nodes\n32 racks)",
    "System 14\n(1024 nodes\n32 racks)"
]

MIN_VAL = 1e-12

# ── Data ──────────────────────────────────────────────────────
data = {
    'r9_flat': {
        4:  {'PDL': 1.000000e+00, 'NOMDL': 1.378418e-06, 'BR': 9.994000e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 1.897643e-06, 'BR': 6.516194e-04},
        6:  {'PDL': 6.472222e-01, 'NOMDL': 8.742048e-07, 'BR': 4.905083e-04},
        7:  {'PDL': 3.944444e-01, 'NOMDL': 5.130434e-07, 'BR': 3.782500e-04},
        8:  {'PDL': 2.500000e-01, 'NOMDL': 3.178927e-07, 'BR': 4.171778e-04},
        13: {'PDL': 5.555556e-03, 'NOMDL': 7.064281e-09, 'BR': 2.747500e-04},
    },
    'r5_hier': {
        4:  {'PDL': 1.000000e+00, 'NOMDL': 1.605358e-06, 'BR': 8.386889e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 2.412452e-06, 'BR': 6.565222e-04},
        6:  {'PDL': 7.250000e-01, 'NOMDL': 1.077303e-06, 'BR': 4.233444e-04},
        7:  {'PDL': 1.916667e-01, 'NOMDL': 2.437177e-07, 'BR': 2.983694e-04},
        8:  {'PDL': 1.000000e+00, 'NOMDL': 1.678650e-06, 'BR': 2.858889e-04},
        13: {'PDL': 2.777778e-03, 'NOMDL': 3.532141e-09, 'BR': 2.341806e-04},
    },
    'r4_hier': {
        4:  {'PDL': 9.833333e-01, 'NOMDL': 2.196108e-06, 'BR': 7.405417e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 2.891057e-06, 'BR': 6.525028e-04},
        6:  {'PDL': 7.555556e-01, 'NOMDL': 1.117922e-06, 'BR': 3.918694e-04},
        7:  {'PDL': 1.527778e-01, 'NOMDL': 1.977999e-07, 'BR': 2.688833e-04},
        8:  {'PDL': 1.000000e+00, 'NOMDL': 2.153723e-06, 'BR': 2.266389e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 2.150528e-04},
    },
    'r3_hier': {
        4:  {'PDL': 9.944444e-01, 'NOMDL': 4.657127e-06, 'BR': 6.286028e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 5.724717e-06, 'BR': 6.619250e-04},
        6:  {'PDL': 7.611111e-01, 'NOMDL': 1.218588e-06, 'BR': 3.404028e-04},
        7:  {'PDL': 4.722222e-02, 'NOMDL': 6.004639e-08, 'BR': 2.194972e-04},
        8:  {'PDL': 1.000000e+00, 'NOMDL': 2.446007e-06, 'BR': 1.996361e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.876611e-04},
    },
}

configs = ['r9_flat', 'r5_hier', 'r4_hier', 'r3_hier']
labels  = ['r=9 (Flat)', 'r=5 (New)', 'r=4 (New)', 'r=3 (Hierarchical)']
colors  = ['#C0392B', '#E67E22', '#F1C40F', '#1ABC9C']
markers = ['o', 's', '^', 'D', 'v', 'p']
sys_colors = ['#2C3E50','#E74C3C','#3498DB','#2ECC71','#9B59B6','#F39C12']

# ═══════════════════════════════════════════════════════════════
# FIGURE 1 — Extended Bar Chart (like original Fig 9)
# ═══════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(1, 3, figsize=(20, 6))
fig1.suptitle(
    'Fig. 9 (Reproduced + Extended) — Reliability under Trace-Driven Failures\n'
    'RS(9,6) across Flat and Intermediate Hierarchical Placements',
    fontsize=13, fontweight='bold', y=1.04
)

x     = np.arange(len(systems))
width = 0.2

def plot_bars(ax, metric, title, ylabel, use_log):
    for i, (cfg, lbl, col) in enumerate(zip(configs, labels, colors)):
        vals = []
        for tid in trace_ids:
            v = data[cfg][tid][metric]
            if use_log and v == 0.0:
                v = MIN_VAL
            vals.append(v)
        offset = (i - 1.5) * width
        ax.bar(x + offset, vals, width, label=lbl,
               color=col, edgecolor='white', linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(sys_labels, fontsize=7.5, ha='center')
    ax.set_xlabel('System ID', fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    if use_log:
        ax.set_yscale('log')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plot_bars(axes[0], 'PDL',   '(a) PDL',   'PDL',           use_log=True)
plot_bars(axes[1], 'NOMDL', '(b) NOMDL', 'NOMDL (B/B)',   use_log=True)
plot_bars(axes[2], 'BR',    '(c) BR',    'Blocked Ratio', use_log=False)

handles, lbls = axes[0].get_legend_handles_labels()
fig1.legend(handles, lbls, loc='upper center', ncol=4,
            fontsize=10, bbox_to_anchor=(0.5, 1.10), frameon=True)

plt.tight_layout()
