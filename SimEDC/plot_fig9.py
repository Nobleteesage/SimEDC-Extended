import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── All 18 results ────────────────────────────────────────────
# System IDs for x-axis (trace_id 13 = System 14)
systems    = [4, 5, 6, 7, 8, 14]
trace_ids  = [4, 5, 6, 7, 8, 13]

data = {
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

# ── Plot settings ─────────────────────────────────────────────
configs = ['rs96_flat', 'rs96_hie', 'drc963']
labels  = ['RS(9,6), r=9', 'RS(9,6), r=3', 'DRC(9,6,3)']
colors  = ['#C0392B', '#E67E22', '#1ABC9C']
x       = np.arange(len(systems))
width   = 0.25
MIN_VAL = 1e-12   # floor for log scale (replace zeros)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Fig. 9 — Reliability under Trace-Driven Failures',
             fontsize=13, fontweight='bold', y=1.02)

def plot_metric(ax, metric, title, ylabel, use_log):
    for i, (cfg, lbl, col) in enumerate(zip(configs, labels, colors)):
        vals = []
        for tid in trace_ids:
            v = data[cfg][tid][metric]
            if use_log and v == 0.0:
                v = MIN_VAL   # avoid log(0)
            vals.append(v)
        offset = (i - 1) * width
        ax.bar(x + offset, vals, width, label=lbl,
               color=col, edgecolor='white', linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in systems])
    ax.set_xlabel('System ID', fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    if use_log:
        ax.set_yscale('log')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plot_metric(axes[0], 'PDL',   '(a) PDL',   'PDL',   use_log=True)
plot_metric(axes[1], 'NOMDL', '(b) NOMDL', 'NOMDL (bytes/byte)', use_log=True)
plot_metric(axes[2], 'BR',    '(c) BR',    'BR',    use_log=False)

# Shared legend
handles, lbls = axes[0].get_legend_handles_labels()
fig.legend(handles, lbls, loc='upper center', ncol=3,
           fontsize=10, bbox_to_anchor=(0.5, 1.08), frameon=True)

plt.tight_layout()
plt.savefig('fig9_reproduced.png', dpi=300, bbox_inches='tight')
plt.savefig('fig9_reproduced.pdf', bbox_inches='tight')
print("✅ Fig. 9 saved as fig9_reproduced.png and fig9_reproduced.pdf")
