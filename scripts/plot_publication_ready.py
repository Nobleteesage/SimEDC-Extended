import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ── Wong (2011) colorblind-safe palette ───────────────────────
# Universally accepted — used in Nature, IEEE, Science
BLUE   = '#0072B2'   # HDD
ORANGE = '#E69F00'   # SSD
GREEN  = '#009E73'   # NVMe
BLACK  = '#000000'
GREY   = '#999999'

# ── Typography for IEEE journal column width ──────────────────
TITLE_SIZE  = 13
LABEL_SIZE  = 11
TICK_SIZE   = 10
LEGEND_SIZE = 9
ANNOT_SIZE  = 8

# ── Systems ───────────────────────────────────────────────────
systems    = [4, 5, 6, 7, 8, 14]
trace_ids  = [4, 5, 6, 7, 8, 13]
sys_labels = [
    "Sys 4\n(128n)",
    "Sys 5\n(128n)",
    "Sys 6\n(256n)",
    "Sys 7\n(256n)",
    "Sys 8\n(512n)",
    "Sys 14\n(1024n)"
]

MIN_VAL    = 1e-12
ITERS      = 360   # used for RE calculation

# ── Relative error calculation (from SimEDC paper Eq.1) ───────
def calc_re(pdl, iters=ITERS):
    """95% confidence interval relative error"""
    if pdl <= 0 or pdl >= 1:
        return 0
    re = (1.96 / pdl) * np.sqrt(pdl * (1 - pdl) / (iters - 1))
    return re * pdl   # return as absolute error for error bars

# ── All results ───────────────────────────────────────────────
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

storage_models = [
    ('HDD\n(Weibull, AFR~4%)',  hdd,  BLUE,   '//'),
    ('SSD\n(Exp., AFR~0.98%)', ssd,  ORANGE, '\\\\'),
    ('NVMe\n(Exp., AFR~0.47%)',nvme, GREEN,  'xx'),
]

configs = [
    ('rs96_flat', 'RS(9,6) r=9 Flat'),
    ('rs96_hie',  'RS(9,6) r=3 Hier.'),
    ('drc963',    'DRC(9,6,3)'),
]

# ═══════════════════════════════════════════════════════════════
# FIGURE 11 — DRC comparison across storage models (FIXED)
# ═══════════════════════════════════════════════════════════════
fig11, axes11 = plt.subplots(1, 3, figsize=(18, 6))
fig11.suptitle(
    'Fig. 11 — DRC(9,6,3) Reliability: HDD vs SSD vs NVMe\n'
    'Wong (2011) colorblind-safe palette | Error bars: 95% CI',
    fontsize=TITLE_SIZE, fontweight='bold', y=1.04
)

x     = np.arange(len(systems))
width = 0.25

def annotate_zero(ax, x_pos, use_log):
    """Annotate bars that are at or below plot minimum"""
    if use_log:
        ax.annotate('≤10⁻¹²',
                    xy=(x_pos, MIN_VAL * 3),
                    fontsize=6, ha='center', color=GREY,
                    rotation=90)

def plot_drc_bars(ax, metric, title, ylabel, use_log):
    for i, (label, data, color, hatch) in enumerate(storage_models):
        vals  = []
        errs  = []
        zeros = []
        for tid in trace_ids:
            v = data['drc963'][tid][metric]
            if v == 0.0:
                zeros.append(True)
                if use_log:
                    v = MIN_VAL
            else:
                zeros.append(False)
            vals.append(v)
            errs.append(calc_re(v) if metric == 'PDL' else 0)

        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width,
                      label=label,
                      color=color,
                      hatch=hatch,
                      edgecolor='white',
                      linewidth=0.8,
                      alpha=0.9)

        # Error bars on PDL only
        if metric == 'PDL':
            ax.errorbar(x + offset, vals, yerr=errs,
                        fmt='none', color='black',
                        capsize=3, linewidth=1.2)

        # Annotate zero bars
        for j, (is_zero, xp) in enumerate(zip(zeros, x + offset)):
            if is_zero and use_log:
                ax.text(xp, MIN_VAL * 5, '▼',
                        ha='center', va='bottom',
                        fontsize=7, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(sys_labels, fontsize=TICK_SIZE)
    ax.set_xlabel('System ID (node count)', fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.set_title(title, fontsize=TITLE_SIZE, fontweight='bold')
    ax.tick_params(axis='both', labelsize=TICK_SIZE)
    if use_log:
        ax.set_yscale('log')
    ax.grid(axis='y', linestyle='--', alpha=0.35, color=GREY)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plot_drc_bars(axes11[0], 'PDL',   '(a) PDL',
              'Probability of Data Loss', use_log=True)
plot_drc_bars(axes11[1], 'NOMDL', '(b) NOMDL',
              'NOMDL (bytes/byte)',       use_log=True)
plot_drc_bars(axes11[2], 'BR',    '(c) Blocked Ratio',
              'Blocked Ratio',           use_log=False)

handles11, lbls11 = axes11[0].get_legend_handles_labels()
fig11.legend(handles11, lbls11,
             loc='upper center', ncol=3,
             fontsize=LEGEND_SIZE,
             bbox_to_anchor=(0.5, 1.12),
             frameon=True,
             edgecolor=GREY)

plt.tight_layout()
plt.savefig('fig11_drc_storage_comparison.png',
            dpi=300, bbox_inches='tight')
plt.savefig('fig11_drc_storage_comparison.pdf',
            bbox_inches='tight')
plt.close()
print("✅ Saved fig11_drc_storage_comparison.png + .pdf")

# ═══════════════════════════════════════════════════════════════
# FIGURES 12a, 12b, 12c — Split into 3 separate figures
# One per storage model — each showing all 3 erasure configs
# ═══════════════════════════════════════════════════════════════

config_colors  = [BLUE, ORANGE, GREEN]
config_markers = ['o', 's', '^']
config_lines   = ['-', '--', ':']
config_labels  = ['RS(9,6) r=9 (Flat)',
                  'RS(9,6) r=3 (Hierarchical)',
                  'DRC(9,6,3)']

for fig_num, (storage_label, data, storage_color, hatch) in \
        enumerate(storage_models):

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Clean storage label for title
    clean_label = storage_label.replace('\n', ' ')
    fig.suptitle(
        f'Fig. 12{"abc"[fig_num]} — {clean_label} Storage: '
        f'Reliability across Erasure Code Configurations\n'
        f'PDL | NOMDL | Blocked Ratio across 6 HPC Systems',
        fontsize=TITLE_SIZE, fontweight='bold', y=1.06
    )

    metrics_info = [
        ('PDL',   '(a) Probability of Data Loss',
         'Probability of Data Loss (PDL)', True),
        ('NOMDL', '(b) Normalised Magnitude of Data Loss',
         'NOMDL (bytes/byte)',              True),
        ('BR',    '(c) Blocked Ratio',
         'Blocked Ratio',                  False),
    ]

    for col, (metric, title, ylabel, use_log) in \
            enumerate(metrics_info):
        ax = axes[col]

        for j, (cfg_key, cfg_label) in enumerate(configs):
            vals = []
            errs = []
            for tid in trace_ids:
                v = data[cfg_key][tid][metric]
                if use_log and v == 0.0:
                    v = MIN_VAL
                vals.append(v)
                errs.append(calc_re(v) if metric == 'PDL' else 0)

            ax.plot(range(len(systems)), vals,
                    color=config_colors[j],
                    marker=config_markers[j],
                    linestyle=config_lines[j],
                    linewidth=2.5,
                    markersize=8,
                    label=cfg_label)

            # Error bars on PDL
            if metric == 'PDL':
                ax.errorbar(range(len(systems)), vals,
                            yerr=errs,
                            fmt='none',
                            color=config_colors[j],
                            capsize=3,
                            linewidth=1,
                            alpha=0.6)

        ax.set_xticks(range(len(systems)))
        ax.set_xticklabels(sys_labels, fontsize=TICK_SIZE)
        ax.set_xlabel('System ID (node count)', fontsize=LABEL_SIZE)
        ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
        ax.set_title(title, fontsize=LABEL_SIZE,
                     fontweight='bold')
        ax.tick_params(axis='both', labelsize=TICK_SIZE)
        if use_log:
            ax.set_yscale('log')
        ax.grid(linestyle='--', alpha=0.35, color=GREY)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if col == 0:
            ax.legend(fontsize=LEGEND_SIZE,
                      loc='upper right',
                      framealpha=0.9,
                      edgecolor=GREY)

    plt.tight_layout()
    suffix = 'abc'[fig_num]
    fname  = f'fig12{suffix}_{"hdd" if fig_num==0 else "ssd" if fig_num==1 else "nvme"}'
    plt.savefig(f'{fname}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{fname}.pdf', bbox_inches='tight')
    plt.close()
    print(f"✅ Saved {fname}.png + .pdf")

print("\n🎉 All publication-ready figures saved!")
print("\nFiles generated:")
print("  fig11_drc_storage_comparison.png/.pdf")
print("  fig12a_hdd.png/.pdf")
print("  fig12b_ssd.png/.pdf")
print("  fig12c_nvme.png/.pdf")
