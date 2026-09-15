import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 8,
    'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
})

dev = pd.read_csv('instrument_deviation.csv')
dec = pd.read_csv('deviation_decomposition.csv')

order = (dec.groupby('analyte')['max_abs_total'].max()
           .sort_values(ascending=False).index.tolist())
levels = ['L1', 'L2', 'L3']
labels, ypos, y = [], [], 0.0
for an in order:
    for lv in levels:
        if not dev[(dev.analyte == an) & (dev.level == lv)].empty:
            labels.append(f'{an}  {lv}' if lv == 'L1' else f'{" "*len(an)}  {lv}')
            ypos.append(y); y += 1
    y += 0.6

key = {(a, l): p for (a, l), p in zip(
    [(labels[i].strip().split('  ')[0], labels[i].strip().split('  ')[-1]) for i in range(len(labels))],
    ypos)}
rowmap = {}
i = 0
for an in order:
    for lv in levels:
        if not dev[(dev.analyte == an) & (dev.level == lv)].empty:
            rowmap[(an, lv)] = ypos[i]; i += 1

markers = {'XR1': ('o', 'black', 'white'), 'XR2': ('s', 'black', '0.55'), 'XR3': ('^', 'black', 'black')}

fig, ax = plt.subplots(figsize=(6.7, 8.6))
for t, ls in ((0, '-'), (1, '--'), (-1, '--'), (2, ':'), (-2, ':')):
    ax.axvline(t, color='0.35' if t == 0 else '0.7', lw=0.7 if t == 0 else 0.5, ls=ls, zorder=0)

for _, r in dev.iterrows():
    yy = rowmap.get((r.analyte, r.level))
    if yy is None: continue
    m, ec, fc = markers[r.instrument]
    ax.plot(r.deviation_sd, yy, marker=m, ms=4.4, mec=ec, mfc=fc, mew=0.7, ls='none', zorder=3)

# connect the three analysers per row
for (an, lv), yy in rowmap.items():
    s = dev[(dev.analyte == an) & (dev.level == lv)].deviation_sd
    if len(s) > 1:
        ax.plot([s.min(), s.max()], [yy, yy], color='0.6', lw=0.6, zorder=1)

ax.set_yticks(list(rowmap.values()))
ax.set_yticklabels([f'{a}  {l}' if l == 'L1' else f'{l}' for (a, l) in rowmap.keys()], fontsize=7)
ax.invert_yaxis()
ax.set_xlabel('Deviation of the analyser mean from the target in force (SD units)', fontsize=8)
ax.set_xlim(-2.7, 2.7)
ax.set_ylim(max(rowmap.values()) + 1.2, min(rowmap.values()) - 1.2)
ax.tick_params(axis='x', labelsize=8)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(False)

handles = [Line2D([], [], marker=m, ls='none', ms=4.4, mec=ec, mfc=fc, mew=0.7, label=k)
           for k, (m, ec, fc) in markers.items()]
ax.legend(handles=handles, loc='lower right', frameon=False, fontsize=7.5,
          handletextpad=0.4, borderaxespad=0.6)

fig.tight_layout()
fig.savefig('/mnt/user-data/outputs/Figure3_instrument_deviation.tif',
            dpi=300, format='tiff', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig('/mnt/user-data/outputs/Figure3_instrument_deviation.png', dpi=300)
print('saved. rows:', len(rowmap))
print('x range of data: %.2f to %.2f' % (dev.deviation_sd.min(), dev.deviation_sd.max()))
