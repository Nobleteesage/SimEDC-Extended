import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Systems ───────────────────────────────────────────────────
systems    = [4, 5, 6, 7, 8, 14]
trace_ids  = [4, 5, 6, 7, 8, 13]
sys_labels = [
    "System 4\n(128 nodes)",
    "System 5\n(128 nodes)",
    "System 6\n(256 nodes)",
    "System 7\n(256 nodes)",
    "System 8\n(512 nodes)",
    "System 14\n(1024 nodes)"
]

MIN_VAL = 1e-12

# ── HDD Results (original reproduction) ───────────────────────
hdd = {
    'rs96_flat': {
        4:  {'PDL': 1.000000e+00, 'NOMDL': 1.378418e-06, 'BR': 9.994000e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 1.897643e-06, 'BR': 6.516194e-04},
        6:  {'PDL': 6.472222e-01, 'NOMDL': 8.742048e-07, 'BR': 4.905083e-04},
        7:  {'PDL': 3.944444e-01, 'NOMDL': 5.130434e-07, 'BR': 3.782500e-04},
        8:  {'PDL': 2.500000e-01, 'NOMDL': 3.178927e-07, 'BR': 4.171778e-04},
        13: {'PDL': 5.555556e-03, 'NOMDL': 7.064281e-09, 'BR': 2.747500e-04},
    },
    'rs96_hie': {
        4:  {'PDL': 9.944444e-01, 'NOMDL': 4.657127e-06, 'BR': 6.286028e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 5.724717e-06, 'BR': 6.619250e-04},
        6:  {'PDL': 7.611111e-01, 'NOMDL': 1.218588e-06, 'BR': 3.404028e-04},
        7:  {'PDL': 4.722222e-02, 'NOMDL': 6.004639e-08, 'BR': 2.194972e-04},
        8:  {'PDL': 1.000000e+00, 'NOMDL': 2.446007e-06, 'BR': 1.996361e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.876611e-04},
    },
    'drc963': {
        4:  {'PDL': 9.750000e-01, 'NOMDL': 3.909197e-06, 'BR': 3.454639e-04},
        5:  {'PDL': 1.000000e+00, 'NOMDL': 2.408920e-06, 'BR': 3.668250e-04},
        6:  {'PDL': 3.972222e-01, 'NOMDL': 5.757389e-07, 'BR': 1.668528e-04},
        7:  {'PDL': 2.222222e-02, 'NOMDL': 2.825712e-08, 'BR': 1.237917e-04},
        8:  {'PDL': 1.000000e+00, 'NOMDL': 2.212886e-06, 'BR': 1.462611e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.098111e-04},
    },
}

# ── SSD Results ───────────────────────────────────────────────
ssd = {
    'rs96_flat': {
        4:  {'PDL': 7.166667e-01, 'NOMDL': 9.545610e-07, 'BR': 2.486583e-04},
        5:  {'PDL': 7.305556e-01, 'NOMDL': 9.510288e-07, 'BR': 2.505111e-04},
        6:  {'PDL': 6.388889e-02, 'NOMDL': 8.123923e-08, 'BR': 2.517389e-04},
        7:  {'PDL': 8.055556e-02, 'NOMDL': 1.024321e-07, 'BR': 2.506167e-04},
        8:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 2.311750e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 2.305000e-04},
    },
    'rs96_hie': {
        4:  {'PDL': 7.500000e-02, 'NOMDL': 9.889994e-08, 'BR': 2.062694e-04},
        5:  {'PDL': 5.833333e-02, 'NOMDL': 7.417495e-08, 'BR': 2.073028e-04},
        6:  {'PDL': 1.111111e-02, 'NOMDL': 1.412856e-08, 'BR': 1.938000e-04},
        7:  {'PDL': 1.388889e-02, 'NOMDL': 1.766070e-08, 'BR': 1.938194e-04},
        8:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.789750e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.789556e-04},
    },
    'drc963': {
        4:  {'PDL': 5.000000e-02, 'NOMDL': 6.357853e-08, 'BR': 1.439250e-04},
        5:  {'PDL': 3.055556e-02, 'NOMDL': 4.591783e-08, 'BR': 1.437111e-04},
        6:  {'PDL': 1.111111e-02, 'NOMDL': 1.412856e-08, 'BR': 1.379528e-04},
        7:  {'PDL': 2.777778e-03, 'NOMDL': 3.532141e-09, 'BR': 1.391083e-04},
        8:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.298472e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.306500e-04},
    },
}

# ── NVMe Results ──────────────────────────────────────────────
nvme = {
    'rs96_flat': {
        4:  {'PDL': 5.194444e-01, 'NOMDL': 6.790540e-07, 'BR': 2.324944e-04},
        5:  {'PDL': 2.083333e-01, 'NOMDL': 2.684427e-07, 'BR': 2.129833e-04},
        6:  {'PDL': 1.666667e-02, 'NOMDL': 2.119284e-08, 'BR': 2.166861e-04},
        7:  {'PDL': 4.166667e-02, 'NOMDL': 5.298211e-08, 'BR': 2.279361e-04},
        8:  {'PDL': 5.555556e-03, 'NOMDL': 7.064281e-09, 'BR': 2.184667e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 2.159028e-04},
    },
    'rs96_hie': {
        4:  {'PDL': 3.333333e-02, 'NOMDL': 4.238569e-08, 'BR': 1.895639e-04},
        5:  {'PDL': 2.222222e-02, 'NOMDL': 2.825712e-08, 'BR': 1.697667e-04},
        6:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.704472e-04},
        7:  {'PDL': 2.777778e-03, 'NOMDL': 3.532141e-09, 'BR': 1.781472e-04},
        8:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.721389e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.698083e-04},
    },
    'drc963': {
        4:  {'PDL': 2.500000e-02, 'NOMDL': 3.178927e-08, 'BR': 1.355694e-04},
        5:  {'PDL': 1.111111e-02, 'NOMDL': 1.412856e-08, 'BR': 1.259833e-04},
        6:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.261583e-04},
        7:  {'PDL': 2.777778e-03, 'NOMDL': 3.532141e-09, 'BR': 1.305528e-04},
        8:  {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.277444e-04},
        13: {'PDL': 0.000000e+00, 'NOMDL': 0.000000e+00, 'BR': 1.266222e-04},
    },
}

# ── Plot settings ─────────────────────────────────────────────
storage_models = [
    ('HDD', hdd, '#C0392B', 'o'),
    ('SSD', ssd, '#E67E22', 's'),
    ('NVMe', nvme, '#1ABC9C', '^'),
]

erasure_configs = [
    ('rs96_flat', 'RS(9,6) Flat r=9',   '-'),
    ('rs96_hie',  'RS(9,6) Hier. r=3',  '--'),
    ('drc963',    'DRC(9,6,3)',          ':'),
]

# ═══════════════════════════════════════════════════════════════
# FIGURE 1 — Bar chart: DRC comparison across storage models
# ═══════════════════════════════════════════════════════════════
fig1, axes1 = plt.subplots(1, 3, figsize=(20, 6))
fig1.suptitle(
    'Fig. 11 — HDD vs SSD vs NVMe: DRC(9,6,3) Reliability Comparison\n'
    'Does DRC maintain its advantage under modern flash storage failure models?',
    fontsize=12, fontweight='bold', y=1.04
)

x     = np.arange(len(systems))
width = 0.25
colors_storage = ['#C0392B', '#E67E22', '#1ABC9C']

def plot_storage_bars(ax, metric, title, ylabel, use_log):
    for i, (label, data, color, marker) in enumerate(storage_models):
        vals = []
        for tid in trace_ids:
            v = data['drc963'][tid][metric]
            if use_log and v == 0.0:
                v = MIN_VAL
            vals.append(v)
        offset = (i - 1) * width
        ax.bar(x + offset, vals, width, label=f'DRC — {label}',
               color=color, edgecolor='white', linewidth=0.5,
               alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(sys_labels, fontsize=8)
    ax.set_xlabel('System ID', fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=11, fontweight='bold')
    if use_log:
        ax.set_yscale('log')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plot_storage_bars(axes1[0], 'PDL',   '(a) PDL',   'PDL',          use_log=True)
plot_storage_bars(axes1[1], 'NOMDL', '(b) NOMDL', 'NOMDL (B/B)',  use_log=True)
plot_storage_bars(axes1[2], 'BR',    '(c) BR',    'Blocked Ratio',use_log=False)

handles1, lbls1 = axes1[0].get_legend_handles_labels()
fig1.legend(handles1, lbls1, loc='upper center', ncol=3,
            fontsize=10, bbox_to_anchor=(0.5, 1.10), frameon=True)

plt.tight_layout()
plt.savefig('fig11_drc_storage_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved fig11_drc_storage_comparison.png")

# ═══════════════════════════════════════════════════════════════
# FIGURE 2 — Line chart: all configs across all storage models
# ═══════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(3, 3, figsize=(20, 16))
fig2.suptitle(
    'Fig. 12 — Full Reliability Comparison: HDD vs SSD vs NVMe\n'
    'Across RS(9,6) Flat, RS(9,6) Hierarchical, and DRC(9,6,3)',
    fontsize=13, fontweight='bold', y=1.02
)

metrics = [
    ('PDL',   '(a) PDL',   'PDL',          True),
    ('NOMDL', '(b) NOMDL', 'NOMDL (B/B)',  True),
    ('BR',    '(c) BR',    'Blocked Ratio', False),
]

storage_colors = {
    'HDD':  '#C0392B',
    'SSD':  '#E67E22',
    'NVMe': '#1ABC9C',
}
config_styles = {
    'rs96_flat': '-',
    'rs96_hie':  '--',
    'drc963':    ':',
}
config_labels = {
    'rs96_flat': 'RS Flat r=9',
    'rs96_hie':  'RS Hier. r=3',
    'drc963':    'DRC(9,6,3)',
}

for row, (storage_label, data, color, marker) in enumerate(storage_models):
    for col, (metric, title, ylabel, use_log) in enumerate(metrics):
        ax = axes2[row][col]
        for cfg, linestyle in config_styles.items():
            vals = []
            for tid in trace_ids:
                v = data[cfg][tid][metric]
                if use_log and v == 0.0:
                    v = MIN_VAL
                vals.append(v)
            ax.plot(range(len(systems)), vals,
                    linestyle=linestyle,
                    marker=marker,
                    color=color,
                    linewidth=2,
                    markersize=7,
                    label=config_labels[cfg])
        ax.set_xticks(range(len(systems)))
        ax.set_xticklabels([f"S{s}" for s in systems], fontsize=8)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.set_title(f'{storage_label} — {title}',
                     fontsize=10, fontweight='bold')
        if use_log:
            ax.set_yscale('log')
        ax.grid(linestyle='--', alpha=0.4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if row == 0 and col == 0:
            ax.legend(fontsize=8, loc='upper right')

plt.tight_layout()
plt.savefig('fig12_full_storage_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved fig12_full_storage_comparison.png")
print("\n🎉 All comparison figures generated successfully!")
print("\nKey findings to note:")
print("1. DRC maintains lowest BR across ALL storage models")
print("2. SSD/NVMe show dramatically lower PDL than HDD")
print("3. Systems 8 & 14 achieve near-zero PDL under SSD/NVMe")
print("4. The DRC advantage is preserved regardless of storage type")
